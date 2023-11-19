from marshmallow import Schema, fields
from extensions import ma


class RestrictionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump=True)
    name = fields.Str()


restriction_schema = RestrictionSchema()
restrictions_schema = RestrictionSchema(many=True)
