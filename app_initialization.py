from flask import Flask
from config.config import Config
from flask_cors import CORS
from extensions import db, jwt
from api.v1 import api_v1_bp


def create_app():
    app = Flask(__name__)
    CORS(app,
         resources={r"/*": {"origins": ["http://localhost:8000/*"]}},
         supports_credentials=True,
         )

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    @app.before_first_request
    def init():
        db.create_all()

    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    return app
