from extensions import db, ma, fields
from datetime import datetime

from sqlalchemy import Integer, String,  ForeignKey, DateTime, Column, UniqueConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref

from .constraints import Constraint
from .qualifications import Qualification, QualificationSchema
from .day_off_requests import DayOffRequest
from .shifts import Shift
from .employee_types import EmployeeType, EmployeeTypeSchema
from .employee_constraints import EmployeeConstraint, EmployeeConstraintSchema


employee_qualifications = db.Table(
    "employee_qualifications",
    Column('employee_id', ForeignKey('employees.employee_id', ondelete="CASCADE")),
    Column('qualification_id', ForeignKey('qualifications.qualification_id', ondelete="CASCADE")),
    UniqueConstraint('employee_id', 'qualification_id', name='uq_employee_qualification')

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
    dependencies = relationship(
        'Dependency',
        foreign_keys='Dependency.employee_id',
        back_populates='employee',
        cascade='all, delete-orphan'
    )

    dependents = relationship(
        'Dependency',
        foreign_keys='Dependency.dependent_employee_id',
        back_populates='dependent_employee',
        cascade='all, delete-orphan'
    )
    # Many to One
    employee_type: Mapped["EmployeeType"] = relationship(backref='employees')

    # Many to Many
    qualifications: Mapped[list[Qualification]] = relationship(
        secondary=employee_qualifications, backref=backref('employees', passive_deletes=True))
    # many-to-many relationship to Constraint, bypassing the `EmployeeConstraint` class
    constraints: Mapped[list["Constraint"]] = relationship(
        secondary="employee_constraints", backref='employees', viewonly=True)
    # association between Employee -> EmployeeConstraint -> Constraint
    employee_constraints: Mapped[list["EmployeeConstraint"]] = relationship(
        backref='employees', cascade="all, delete-orphan", passive_deletes=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)


class Dependency(db.Model):
    __tablename__ = 'dependencies'

    dependency_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.employee_id', ondelete="CASCADE"), nullable=False)
    dependent_employee_id: Mapped[int] = mapped_column(ForeignKey(
        'employees.employee_id', ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)
    __table_args__ = (
        UniqueConstraint('employee_id', 'dependent_employee_id',
                         name='uq_dependency'),
    )
    employee = relationship('Employee', foreign_keys=[employee_id], back_populates='dependencies')
    dependent_employee = relationship('Employee', foreign_keys=[dependent_employee_id], back_populates='dependents')


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee

    employee_type = fields.Nested(EmployeeTypeSchema)
    qualifications = fields.Nested(QualificationSchema, many=True)
    employee_constraints = fields.Nested(EmployeeConstraintSchema, many=True)
    dependencies = fields.Nested('DependencySchema', many=True)


class DependencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dependency
    created_at = ma.auto_field(load_only=True)
    updated_at = ma.auto_field(load_only=True)
    dependent_employee = fields.Nested("EmployeeSchema", only=('employee_id', 'first_name', 'last_name'))
