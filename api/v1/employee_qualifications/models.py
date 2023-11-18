from extensions  import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,desc
from sqlalchemy.orm import relationship

class EmployeeQualification(db.Model):
    __tablename__ = 'employee_qualifications'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    qualification_id = Column(Integer, ForeignKey('qualifications.id'))

    employee = relationship("Employee", back_populates="qualifications")
    qualification = relationship("Qualification", back_populates="employees")
