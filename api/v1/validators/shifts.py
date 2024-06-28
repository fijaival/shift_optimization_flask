from marshmallow import Schema, fields, validate


class PostShiftsSchema(Schema):
    date = fields.Date(required=True)
    employee_id = fields.Int(required=True)
    shift_number = fields.Int(required=True)
    task_id = fields.Int(required=True)


post_shifts_schema = PostShiftsSchema(many=True)
