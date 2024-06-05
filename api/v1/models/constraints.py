from extensions import db
from datetime import datetime


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Constraint(db.Model):
    __tablename__ = 'constraints'

    constraint_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee_constraints = relationship(
        "EmployeeConstraint", back_populates="constraint", cascade='all, delete-orphan')
    facility_constraints = relationship(
        "FacilityConstraint", back_populates="constraint", cascade='all, delete-orphan')
