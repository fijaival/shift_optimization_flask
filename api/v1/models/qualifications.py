from extensions import db, ma
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Qualification(db.Model):
    __tablename__ = 'qualifications'

    qualification_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)


class QualificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Qualification
