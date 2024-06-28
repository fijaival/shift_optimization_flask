from extensions import Base, ma
from datetime import datetime
from datetime import date as dt_date

from sqlalchemy import String, UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column


class Shift(Base):
    __tablename__ = 'shifts'

    shift_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey(
        'employees.employee_id', ondelete="CASCADE"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey(
        "tasks.task_id", ondelete="CASCADE"), nullable=False)
    date: Mapped[dt_date] = mapped_column(nullable=False)
    shift_number: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', "task_id", name='uq_shift'),
    )


class ShiftSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shift
    created_at = ma.auto_field(load_only=True)
    updated_at = ma.auto_field(load_only=True)
