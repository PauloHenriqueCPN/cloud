from flask_restful import Resource, reqparse

class PlaylistController(Resource):
    def __init__(self, cosmos_client):
        self.container = cosmos_client.get_database_client("spotify").get_container_client("playlist")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Nome da playlist necessário")
        parser.add_argument("user_id", required=True, help="ID do usuário necessário")
        data = parser.parse_args()

        playlist = {
            "id": f"{data['user_id']}_{data['name']}",
            "name": data["name"],
            "user_id": data["user_id"]
        }

        self.container.upsert_item(playlist)
        return {"mensagem": "Playlist criada com sucesso", "playlist": playlist}, 201

    def get(self, user_id):
        try:
            query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
            playlist = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            if not playlist:
                return {"mensagem": "Nenhuma playlist encontrada para este usuário"}, 404
            return {"playlists": playlist}, 200
        except Exception:
            return {"mensagem": "Erro ao procurar playlist"}, 500
