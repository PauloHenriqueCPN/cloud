from flask import Flask
from flask_restful import Api
from app.controllers.userController import UserController
from app.controllers.playlistController import PlaylistController
from app.controllers.musicController import MusicController
from app.config import cosmos_client, COSMOS_DB_NAME
from azure.cosmos import PartitionKey

def setup_containers():
    print("Setting up database and containers...")
    database = cosmos_client.create_database_if_not_exists(COSMOS_DB_NAME)

    database.create_container_if_not_exists(id="user", partition_key=PartitionKey(path="/id"))
    database.create_container_if_not_exists(id="playlist", partition_key=PartitionKey(path="/user_id"))
    database.create_container_if_not_exists(id="music", partition_key=PartitionKey(path="/playlist_id"))
    print("Containers created or verified successfully!")

setup_containers()

# Função para criar o app Flask
def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Rotas de Usuários
    api.add_resource(
        UserController,
        "/api/user",
        "/api/user/<string:user_id>",
        resource_class_args=(cosmos_client,)
    )

    # Rotas de Playlists
    api.add_resource(
        PlaylistController,
        "/api/playlist",
        "/api/playlist/<string:user_id>",
        resource_class_args=(cosmos_client,)
    )

    # Rotas de Músicas
    api.add_resource(
        MusicController,
        "/api/music",
        "/api/music/<string:playlist_id>",
        resource_class_args=(cosmos_client,)
    )

    return app
