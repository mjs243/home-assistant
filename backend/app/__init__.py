from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    # Register blueprints or routes here
    from app.routes import api_blueprint
    from app.docker_control import docker_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(docker_blueprint, url_prefix="/api")

    return app