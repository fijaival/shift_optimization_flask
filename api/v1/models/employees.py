from extensions import db
from datetime import datetime

from sqlalchemy import Integer, String,  ForeignKey, DateTime, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref

from .constraints import Constraint
from .qualifications import Qualification
from .day_off_requests import DayOffRequest
from .shifts import Shift
from .dependencies import Dependency
from .employee_types import EmployeeType
from .employee_constraints import EmployeeConstraint


employee_qualifications = db.Table(
    "employee_qualifications",
    Column('employee_id', ForeignKey('employees.employee_id', ondelete="CASCADE")),
    Column('qualification_id', ForeignKey('qualifications.qualification_id', ondelete="CASCADE"))
)


class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'facilities.facility_id', ondelete='RESTRICT'), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    employee_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('employee_types.employee_type_id', ondelete='RESTRICT'), nullable=False)

    # One to Many
    day_off_requests: Mapped[list["DayOffRequest"]] = relationship(
        backref='employee', cascade="all, delete-orphan", passive_deletes=True,)
    shifts: Mapped[list["Shift"]] = relationship(
        backref='employee', cascade="all, delete-orphan", passive_deletes=True,)
    dependencies: Mapped[list["Dependency"]] = relationship(
        foreign_keys='Dependency.employee_id', backref='employee', cascade="all, delete-orphan", passive_deletes=True,)
    dependent_employees: Mapped[list["Dependency"]] = relationship(
        foreign_keys='Dependency.dependent_employee_id', backref='dependent_employee', cascade="all, delete-orphan", passive_deletes=True,)

    # Many to One
    employee_type: Mapped["EmployeeType"] = relationship(backref='employees')

    # Many to Many
    qualifications: Mapped[list[Qualification]] = relationship(
        secondary=employee_qualifications, backref=backref('employees', passive_deletes=True))
    # many-to-many relationship to Constraint, bypassing the `EmployeeConstraint` class
    constraints: Mapped[list["Constraint"]] = relationship(
        secondary="employee_constraints", backref=backref('employees', passive_deletes=True), viewonly=True)
    # association between Employee -> EmployeeConstraint -> Constraint
    employee_constraints: Mapped[list["EmployeeConstraint"]] = relationship(backref='employees')

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)
