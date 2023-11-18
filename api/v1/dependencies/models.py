from extensions import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,desc
from sqlalchemy.orm import relationship


class EmployeeDependency(db.Model):
    __tablename__ = 'employee_dependencies'
    
    id = Column(Integer, primary_key=True)
    dependent_employee_id = Column(Integer, ForeignKey('employees.id'))
    required_employee_id = Column(Integer, ForeignKey('employees.id'))

    dependent_employee = relationship("Employee", foreign_keys=[dependent_employee_id], back_populates="dependencies")
    required_employee = relationship("Employee", foreign_keys=[required_employee_id])
