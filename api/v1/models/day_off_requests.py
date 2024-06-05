from extensions import db
from datetime import datetime


from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship


class DayOffRequest(db.Model):
    __tablename__ = 'day_off_requests'

    request_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer,
                         ForeignKey('employees.employee_id'),
                         nullable=False)
    date = Column(Date, nullable=False)
    type_of_vacation = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee = relationship('Employee', back_populates='day_off_requests')

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_day_off_request'),
    )
