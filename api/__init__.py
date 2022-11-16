from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .hepsiburada import hepsiburada
    app.register_blueprint(hepsiburada)
    return app