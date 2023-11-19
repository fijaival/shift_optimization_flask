from marshmallow import Schema, fields


class DriverSchema(Schema):
    id = fields.Int(dump_only=True)
    last_name = fields.Str(required=True)
    first_name = fields.Str(required=True)


# スキーマのインスタンス化
driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)
