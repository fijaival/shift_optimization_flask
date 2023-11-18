from flask import Flask
from config.config import Config
from extensions import db
from api.v1 import api_v1_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.before_first_request
    def init():
        db.create_all()

    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app
