from extensions import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,desc
from sqlalchemy.orm import relationship


class Qualification(db.Model):
    __tablename__ = 'qualifications'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    employees = relationship("EmployeeQualification", back_populates="qualification", cascade='all, delete-orphan')

