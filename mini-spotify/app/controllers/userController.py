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

        query = f"SELECT * FROM c WHERE c.email = '{data['email']}'"
        existing_users = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        
        if existing_users:
            return {"mensagem": "E-mail já cadastrado"}, 400

        user = {
            "id": data["email"],  # Use o e-mail como ID
            "username": data["username"],
            "email": data["email"]
        }

        try:
            self.container.upsert_item(user)
            return {"mensagem": "Usuário criado com sucesso", "usuário": user}, 201
        except Exception as e:
            return {"mensagem": f"Erro ao criar usuário: {str(e)}"}, 500


    def get(self, user_id):
        try:
            user_data = self.container.read_item(item=user_id, partition_key=user_id)
            user = User.from_dict(user_data)
            return {"user": user.to_dict()}, 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar usuário: {str(e)}"}, 404
