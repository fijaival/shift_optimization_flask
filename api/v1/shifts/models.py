from extensions import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Shift(db.Model):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(Date)
    type_of_work = Column(String)

    # Employee relationship
    employee = relationship("Employee", back_populates="shifts")
