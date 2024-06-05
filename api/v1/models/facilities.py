from datetime import datetime
from extensions import db, ma
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Facility(db.Model):
    __tablename__ = 'facilities'
    facility_id = Column(Integer, primary_key=True)
    facility_name = Column(String(191), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employees = relationship('Employee', back_populates='facility')
    users = relationship('User', back_populates='facility')
    facility_constraints = relationship(
        'FacilityConstraint', back_populates="facility", cascade="all, delete-orphan")
    facility_qualifications = relationship(
        'FacilityQualification', back_populates="facility", cascade="all, delete-orphan")
