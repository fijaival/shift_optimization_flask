from extensions import db

from ..dependencies import EmployeeDependency
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship


class Employee(db.Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)

    qualifications = relationship(
        "EmployeeQualification", back_populates="employee")
    restrictions = relationship(
        "EmployeeRestriction", back_populates="employee")
    dependencies = relationship("EmployeeDependency", foreign_keys=[
                                EmployeeDependency.dependent_employee_id], back_populates="dependent_employee")
    shift_requests = relationship('ShiftRequest',  back_populates="employee")
    shifts = relationship('Shift', back_populates='employee')
