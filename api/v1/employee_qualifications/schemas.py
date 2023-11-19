# employee_qualifications/schemas.py
from marshmallow import Schema, fields


class EmployeeQualificationSchema(Schema):
    employee_id = fields.Int(required=True)
    qualification_id = fields.Int(required=True)


# スキーマのインスタンス化
employee_qualification_schema = EmployeeQualificationSchema()
