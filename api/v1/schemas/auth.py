from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


# スキーマのインスタンス化
user_schema = UserSchema()
users_schema = UserSchema(many=True)
