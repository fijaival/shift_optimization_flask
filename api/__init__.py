from flask import Flask, jsonify
from config import Config
from flask_cors import CORS
from extensions import db, jwt
from api.v1 import api_v1_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from .error import InvalidAPIUsage

app = Flask(__name__)

app.config.from_object(Config)
CORS(app,
     resources={r"/*": {"origins": ["http://localhost:8000/*"]}},
     supports_credentials=True,
     )

db.init_app(app)
migrate = Migrate(app, db)


@app.before_first_request
def init():
    db.create_all()


app.register_blueprint(api_v1_bp, url_prefix='/v1')

print(app.config['SQLALCHEMY_DATABASE_URI'])

# InvalidAPIUsageエラーをハンドリング


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    print("よんだよ")
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# JWTのイベントハンドラーの設定


def init_jwt(app):
    jwt.init_app(app)


init_jwt(app)
