from extensions  import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,desc
from sqlalchemy.orm import relationship

class EmployeeRestriction(db.Model):
    __tablename__ = 'employee_restrictions'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    restriction_id = Column(Integer, ForeignKey('restrictions.id'))
    value = Column(Integer)

    employee = relationship("Employee", back_populates="restrictions")
    restriction = relationship("Restriction", back_populates="employees")
