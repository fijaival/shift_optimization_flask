from extensions import db
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, UniqueConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .constraints import Constraint


class EmployeeConstraint(db.Model):
    __tablename__ = 'employee_constraints'

    employee_constraint_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey('employees.employee_id'), nullable=False)
    constraint_id: Mapped[int] = mapped_column(Integer, ForeignKey('constraints.constraint_id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    constraint: Mapped["Constraint"] = relationship(backref='employee_constraints')

    __table_args__ = (
        UniqueConstraint('employee_id', 'constraint_id', name='uq_employee_constraint'),
    )
