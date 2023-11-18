from marshmallow import Schema, fields
from extensions import ma


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
