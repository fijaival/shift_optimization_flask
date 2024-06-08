from extensions import db
from datetime import datetime


from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column


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
