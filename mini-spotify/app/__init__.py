from flask import Flask
from app.routes import create_app

def init_app():
    app = create_app()
    return app
