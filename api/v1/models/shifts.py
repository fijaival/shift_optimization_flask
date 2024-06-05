from extensions import db
from datetime import datetime

from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship


class Shift(db.Model):
    __tablename__ = 'shifts'

    shift_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    date = Column(Date, nullable=False)
    type_of_work = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee = relationship('Employee', back_populates='shifts')

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_shift'),
    )
