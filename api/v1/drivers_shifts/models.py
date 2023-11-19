from extensions import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class DriversShift(db.Model):
    __tablename__ = 'drivers_shifts'

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('drivers.id'))  # 'drivers' テーブルを参照
    date = Column(Date)
    type_of_work = Column(String)

    # Driver relationship
    driver = relationship("Driver", back_populates="drivers_shifts")
