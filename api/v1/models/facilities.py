from datetime import datetime
from extensions import db, ma, fields
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .employees import Employee
from .auth import User
from .constraints import Constraint
from .qualifications import Qualification

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
    facility_id = Column(Integer, primary_key=True)
    facility_name = Column(String(191), nullable=False)
    employees = relationship('Employee', backref='facility')
    users = relationship('User', backref='facility')
    constraints = relationship(
        'Constraint', secondary=facility_constraints, backref="facilities")
    qualifications = relationship(
        'Qualification', secondary=facility_qualifications, backref="facilities")

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)


class FacilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Facility
