from marshmallow import Schema, fields
from extensions import ma


class ShiftSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    employee_id = fields.Int()
    date = fields.Date()
    type_of_work = fields.Str()


shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)
