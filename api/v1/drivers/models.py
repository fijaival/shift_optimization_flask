from extensions import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship


class Driver(db.Model):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)

    drivers_requests = relationship("DriversRequests", back_populates="driver")
    drivers_shifts = relationship("DriversShift", back_populates="driver")
