from marshmallow import Schema, fields
from extensions import ma

class QualificationSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int() 
    name = fields.Str()

qualifications_schema = QualificationSchema(many=True)
