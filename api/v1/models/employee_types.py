from extensions import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class EmployeeType(db.Model):
    __tablename__ = 'employee_types'

    employee_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employees = relationship('Employee', back_populates='employee_type')
