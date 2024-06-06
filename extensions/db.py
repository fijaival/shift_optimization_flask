from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from sqlalchemy.dialects.mysql import TINYINT, VARBINARY
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


ma = Marshmallow()


fields = fields.fields

db.Tinyint = TINYINT
db.Varbinary = VARBINARY
