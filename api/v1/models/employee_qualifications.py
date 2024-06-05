from extensions import db
from datetime import datetime

from sqlalchemy import Column, Integer,  ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship


class EmployeeQualification(db.Model):
    __tablename__ = 'employee_qualifications'

    employee_qualification_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    qualification_id = Column(Integer, ForeignKey(
        'qualifications.qualification_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee = relationship(
        "Employee", back_populates="employee_qualifications")
    qualification = relationship(
        "Qualification", back_populates="employee_qualifications")

    __table_args__ = (
        UniqueConstraint('employee_id', 'qualification_id',
                         name='uq_employee_qualification'),
    )
