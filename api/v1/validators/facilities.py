
from marshmallow import Schema, fields, validate


class PostFacilitySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))


class PostFcilityAtributeSchema(Schema):
    id = fields.Int(required=True)


post_facility_schema = PostFacilitySchema()
post_facility_atrubute_schema = PostFcilityAtributeSchema()
