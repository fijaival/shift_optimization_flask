from extensions import db
from datetime import datetime

from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey(
        'facilities.facility_id'), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    employee_type_id = Column(Integer, ForeignKey(
        'employee_types.employee_type_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee_type = relationship('EmployeeType', back_populates='employees')
    facility = relationship('Facility', back_populates='employees')
    employee_qualifications = relationship(
        'EmployeeQualification', back_populates='employee', cascade="all, delete-orphan")
    employee_constraints = relationship(
        'EmployeeConstraint', back_populates='employee', cascade="all, delete-orphan")
    day_off_requests = relationship(
        'DayOffRequest', back_populates='employee', cascade="all, delete-orphan")
    shifts = relationship(
        'Shift', back_populates='employee', cascade="all, delete-orphan")
    dependencies = relationship('Dependency', foreign_keys='Dependency.employee_id',
                                back_populates='employee', cascade="all, delete-orphan")
    dependent_employees = relationship('Dependency', foreign_keys='Dependency.dependent_employee_id',
                                       back_populates='dependent_employee', cascade="all, delete-orphan")
