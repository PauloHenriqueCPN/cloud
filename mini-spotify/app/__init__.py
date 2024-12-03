from flask import Flask
from app.routes import create_app

# Criação da aplicação Flask
def init_app():
    app = create_app()
    return app
