from marshmallow import Schema, fields
from src import ma



class AttributeSchema(ma.SQLAlchemyAutoSchema):
    employee_id = fields.Int()
    day_qualified = fields.Bool()
    night_qualified = fields.Bool()
    night_shift_incapable = fields.Bool()
    night_shift_only = fields.Bool()
    can_drive = fields.Bool()
    night_shift_max = fields.Int()
    max_continuous_works = fields.Int()
    requid = fields.Int()

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()

class QualificationSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int() 
    name = fields.Str()

class RestrictionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int() 
    name = fields.Str()


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
qualifications_schema = QualificationSchema(many=True)
restriction_schema = RestrictionSchema(many=True)