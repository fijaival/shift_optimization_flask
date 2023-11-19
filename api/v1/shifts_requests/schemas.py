from marshmallow import Schema, fields, validate


class ShiftRequestSchema(Schema):
    employee_id = fields.Int(required=True)
    date = fields.Date(required=True)
    type_of_vacation = fields.Str(
        required=True, validate=validate.OneOf(['有', '公']))


# スキーマのインスタンス化
shift_request_schema = ShiftRequestSchema()
