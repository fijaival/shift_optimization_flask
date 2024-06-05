from flask import Flask
from config import Config
from flask_cors import CORS
from extensions import db
from api.v1 import api_v1_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app,
         resources={r"/*": {"origins": ["http://localhost:8000/*"]}},
         supports_credentials=True,
         )

    jwt.init_app(app)

    db.init_app(app)

    migrate = Migrate(app, db)

    @app.before_first_request
    def init():
        db.create_all()

    app.register_blueprint(api_v1_bp, url_prefix='/v1')

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    return app
