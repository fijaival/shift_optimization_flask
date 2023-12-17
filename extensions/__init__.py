# extensions/__init__.py

from .db import db, jwt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import event
from sqlalchemy.engine import Engine


# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

# Marshmallowのインスタンスを作成
ma = Marshmallow()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()
