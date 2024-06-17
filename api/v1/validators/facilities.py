
from marshmallow import Schema, fields, validate


class PostFacilitySchema(Schema):
    facility_name = fields.Str(
        required=True, validate=validate.Length(min=2, max=50))


class PostQualificationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))


class PostConstraintSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))


post_facility_schema = PostFacilitySchema()
post_qualification_schema = PostQualificationSchema()
post_constraint_schema = PostConstraintSchema()
