from datetime import datetime
from extensions import db, ma, fields
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .employees import Employee
from .auth import User
from .constraints import Constraint, ConstraintSchema
from .qualifications import Qualification, QualificationSchema

facility_constraints = db.Table(
    "facility_constraints",
    Column('facility_id', ForeignKey('facilities.facility_id')),
    Column('constraint_id', ForeignKey('constraints.constraint_id'))
)
facility_qualifications = db.Table(
    "facility_qualifications",
    Column('facility_id', ForeignKey('facilities.facility_id')),
    Column('qualification_id', ForeignKey('qualifications.qualification_id'))
)


class Facility(db.Model):
    __tablename__ = 'facilities'
    facility_id: Mapped[int] = mapped_column(primary_key=True)
    facility_name: Mapped[str] = mapped_column(String(191), nullable=False)

    # One to Many
    employees: Mapped[list["Employee"]] = relationship(backref='facility')
    users: Mapped[list["User"]] = relationship(backref='facility')

    # Many to Many
    constraints: Mapped[list[Constraint]] = relationship(secondary=facility_constraints, backref="facilities")
    qualifications: Mapped[list[Qualification]] = relationship(
        'Qualification', secondary=facility_qualifications, backref="facilities")

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)


class FacilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Facility
    qualifications = fields.Nested(QualificationSchema, many=True)
    constraints = fields.Nested(ConstraintSchema, many=True)
