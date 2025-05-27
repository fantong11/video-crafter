# app/api.py
from flask import Flask
from flasgger import Swagger
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    Swagger(app, template_file=None)  # Use flasgger's default UI at /apidocs
    register_routes(app)
    return app
