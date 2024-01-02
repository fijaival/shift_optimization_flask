from flask import Flask
from config.config import Config
from flask_cors import CORS
from extensions import db, jwt
from api.v1 import api_v1_bp


def create_app():
    app = Flask(__name__)
    CORS(app,
         resources={r"*": {"origins": ["https://localhost:5174/*"]}},
         expose_headers=["X-Access-Token-Csrf", "X-Refresh-Token-Csrf"],
         supports_credentials=True,
         )

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    @app.before_first_request
    def init():
        db.create_all()

    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    # csrf = CSRFProtect()

    # csrf.init_app(app)

    return app
