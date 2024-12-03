from flask_restful import Resource, reqparse

class UserController(Resource):
    def __init__(self, cosmos_client):
        database = cosmos_client.get_database_client("spotify")
        self.container = database.get_container_client("user")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="Nome de usário necessário")
        parser.add_argument("email", required=True, help="Email necessário")
        data = parser.parse_args()

        user = {
            "id": data["email"],  # Use o e-mail como ID
            "username": data["username"],
            "email": data["email"]
        }

        self.container.upsert_item(user)
        return {"mensagem": "Usuário criado com sucesso", "Usuário": user}, 201

    def get(self, user_id):
        try:
            user = self.container.read_item(item=user_id, partition_key=user_id)
            return {"user": user}, 200
        except Exception:
            return {"mensagem": "Usuário não encontrado"}, 404
