from flask_restful import Resource, reqparse
from app.models.user import User

class UserController(Resource):
    def __init__(self, cosmos_client):
        self.container = cosmos_client.get_database_client("spotify").get_container_client("user")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="Nome de usuário necessário")
        parser.add_argument("email", required=True, help="Email necessário")
        data = parser.parse_args()

        try:
            user = User(id=data["email"], username=data["username"], email=data["email"])
            self.container.upsert_item(user.to_dict())
            return {"mensagem": "Usuário criado com sucesso", "usuário": user.to_dict()}, 201
        except Exception as e:
            return {"mensagem": f"Erro ao criar usuário: {str(e)}"}, 500

    def get(self, user_id):
        try:
            user_data = self.container.read_item(item=user_id, partition_key=user_id)
            user = User.from_dict(user_data)
            return {"user": user.to_dict()}, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar usuário: {str(e)}"}, 404
