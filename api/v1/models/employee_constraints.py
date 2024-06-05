from extensions import db
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship


class EmployeeConstraint(db.Model):
    __tablename__ = 'employee_constraints'

    employee_constraint_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    constraint_id = Column(Integer, ForeignKey(
        'constraints.constraint_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee = relationship('Employee', back_populates='')
    constraint = relationship(
        'Constraint', back_populates='employee_constraints')

    __table_args__ = (
        UniqueConstraint('employee_id', 'constraint_id',
                         name='uq_employee_constraint'),
    )
