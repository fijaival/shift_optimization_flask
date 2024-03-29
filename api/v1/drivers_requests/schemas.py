# drivers_requests/schemas.py
from marshmallow import Schema, fields, validate
from datetime import datetime


class DriversRequestSchema(Schema):
    driver_id = fields.Int(required=True)
    date = fields.Date(required=True)
    type_of_vacation = fields.Str(
        required=True, validate=validate.OneOf(['有', '公']))


# スキーマのインスタンス化
drivers_request_schema = DriversRequestSchema()
