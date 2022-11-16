from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .hepsiburada import hepsiburada
    from .google import google
    app.register_blueprint(hepsiburada)
    app.register_blueprint(google)
    return app