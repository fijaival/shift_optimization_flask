
from marshmallow import Schema, fields, validate


class PostFacilitySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))


post_facility_schema = PostFacilitySchema()
