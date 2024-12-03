from flask_restful import Resource, reqparse

class MusicController(Resource):
    def __init__(self, cosmos_client):
        self.container = cosmos_client.get_database_client("spotify").get_container_client("music")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True, help="Título da música necessário")
        parser.add_argument("artist", required=True, help="Artista necessário")
        parser.add_argument("playlist_id", required=True, help="ID da playlist necessário")
        data = parser.parse_args()

        music = {
            "id": f"{data['playlist_id']}_{data['title']}",
            "title": data["title"],
            "artist": data["artist"],
            "playlist_id": data["playlist_id"]
        }

        self.container.upsert_item(music)
        return {"mensagem": "Música adicionada com sucesso", "music": music}, 201

    def get(self, playlist_id):
        try:
            query = f"SELECT * FROM c WHERE c.playlist_id = '{playlist_id}'"
            music = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            if not music:
                return {"mensagem": "Nenhuma música encontrada nesta playlist"}, 404
            return {"músicas": music}, 200
        except Exception:
            return {"mensagem": "Erro ao adicionar música"}, 500
