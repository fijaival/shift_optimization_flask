from extensions import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ShiftRequest(db.Model):
    __tablename__ = 'shifts_requests'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(DateTime)
    type_of_vacation = Column(String(1))

    # Employee モデルとのリレーションシップ（Employee モデルが存在する場合）
    employee = relationship("Employee", back_populates="shift_requests")
