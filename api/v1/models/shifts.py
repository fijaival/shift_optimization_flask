from extensions import db
from datetime import datetime
from datetime import date as dt_date

from sqlalchemy import String, UniqueConstraint, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Shift(db.Model):
    __tablename__ = 'shifts'

    shift_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey(
        'employees.employee_id', ondelete="CASCADE"), nullable=False)
    date: Mapped[dt_date] = mapped_column(Date, nullable=False)
    type_of_work: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_shift'),
    )
