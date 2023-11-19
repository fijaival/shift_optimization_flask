from marshmallow import Schema, fields
from extensions import ma


class DriversShiftSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    driver_id = fields.Int()
    date = fields.Date()
    type_of_work = fields.Str()


drivers_shift_schema = DriversShiftSchema()
drivers_shifts_schema = DriversShiftSchema(many=True)
