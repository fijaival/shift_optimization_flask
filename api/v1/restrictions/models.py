from extensions import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship


class Restriction(db.Model):
    __tablename__ = 'restrictions'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    employees = relationship(
        "EmployeeRestriction", back_populates="restriction", cascade='all, delete-orphan')
