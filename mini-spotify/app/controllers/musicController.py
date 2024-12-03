from flask_restful import Resource, reqparse
from app.models.music import Music

class MusicController(Resource):
    def __init__(self, cosmos_client):
        self.container = cosmos_client.get_database_client("spotify").get_container_client("music")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True, help="Título da música necessário")
        parser.add_argument("artist", required=True, help="Artista necessário")
        parser.add_argument("playlist_id", required=True, help="ID da playlist necessário")
        data = parser.parse_args()

        query = f"SELECT * FROM c WHERE c.title = '{data['title']}' AND c.artist = '{data['artist']}' AND c.playlist_id = '{data['playlist_id']}'"
        existing_music = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        
        if existing_music:
            return {"mensagem": "A música já existe nesta playlist"}, 400

        music = {
            "id": f"{data['playlist_id']}_{data['title']}",
            "title": data["title"],
            "artist": data["artist"],
            "playlist_id": data["playlist_id"]
        }

        try:
            self.container.upsert_item(music)
            return {"mensagem": "Música adicionada com sucesso", "music": music}, 201
        except Exception as e:
            return {"mensagem": f"Erro ao adicionar música: {str(e)}"}, 500


    def get(self, playlist_id):
        try:
            query = f"SELECT * FROM c WHERE c.playlist_id = '{playlist_id}'"
            music_data = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            if not music_data:
                return {"mensagem": "Nenhuma música encontrada nesta playlist"}, 404
            music_list = [Music.from_dict(data).to_dict() for data in music_data]
            return {"músicas": music_list}, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar músicas: {str(e)}"}, 500
