# dependencies/schemas.py
from marshmallow import Schema, fields


class EmployeeDependencySchema(Schema):
    dependent_employee_id = fields.Int(required=True)
    required_employee_id = fields.Int(required=True)


# スキーマのインスタンス化
employee_dependency_schema = EmployeeDependencySchema()
