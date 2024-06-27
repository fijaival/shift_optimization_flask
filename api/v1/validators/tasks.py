from marshmallow import Schema, fields, validate


class PostTaskSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))


post_task_schema = PostTaskSchema()
