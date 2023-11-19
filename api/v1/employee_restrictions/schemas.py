# employees_restrictions/schemas.py
from marshmallow import Schema, fields


class EmployeeRestrictionSchema(Schema):
    employee_id = fields.Int(required=True)
    restriction_id = fields.Int(required=True)
    value = fields.Str(required=True)


# スキーマのインスタンス化
employee_restriction_schema = EmployeeRestrictionSchema()
