from extensions import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class DriversRequests(db.Model):
    __tablename__ = 'drivers_requests'

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    date = Column(DateTime)
    type_of_vacation = Column(String(1))

    # Driver モデルとのリレーションシップ
    driver = relationship("Driver", back_populates="drivers_requests")
