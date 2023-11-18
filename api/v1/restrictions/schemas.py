from marshmallow import Schema, fields
from extensions import ma

class RestrictionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int() 
    name = fields.Str()

restriction_schema = RestrictionSchema(many=True)