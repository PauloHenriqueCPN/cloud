from flask_restful import Resource, reqparse
from app.models.playlist import Playlist

class PlaylistController(Resource):
    def __init__(self, cosmos_client):
        self.container = cosmos_client.get_database_client("spotify").get_container_client("playlist")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Nome da playlist necessário")
        parser.add_argument("user_id", required=True, help="ID do usuário necessário")
        data = parser.parse_args()

        try:
            playlist = Playlist(id=f"{data['user_id']}_{data['name']}", name=data["name"], user_id=data["user_id"])
            self.container.upsert_item(playlist.to_dict())
            return {"mensagem": "Playlist criada com sucesso", "playlist": playlist.to_dict()}, 201
        except Exception as e:
            return {"mensagem": f"Erro ao criar playlist: {str(e)}"}, 500

    def get(self, user_id):
        try:
            query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
            playlists_data = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            if not playlists_data:
                return {"mensagem": "Nenhuma playlist encontrada para este usuário"}, 404
            playlists = [Playlist.from_dict(data).to_dict() for data in playlists_data]
            return {"playlists": playlists}, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar playlists: {str(e)}"}, 500
