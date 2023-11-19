from marshmallow import Schema, fields
from extensions import ma


class QualificationSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


qualification_schema = QualificationSchema()
qualifications_schema = QualificationSchema(many=True)
