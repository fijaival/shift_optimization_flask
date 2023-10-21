from src import db

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,desc
from sqlalchemy.orm import relationship


# DBの作成

class EmployeeDependency(db.Model):
    __tablename__ = 'employee_dependencies'
    
    id = Column(Integer, primary_key=True)
    dependent_employee_id = Column(Integer, ForeignKey('employees.id'))
    required_employee_id = Column(Integer, ForeignKey('employees.id'))

    dependent_employee = relationship("Employee", foreign_keys=[dependent_employee_id], back_populates="dependencies")
    required_employee = relationship("Employee", foreign_keys=[required_employee_id])


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)

    qualifications = relationship("EmployeeQualification", back_populates="employee")
    restrictions = relationship("EmployeeRestriction", back_populates="employee")
    dependencies = relationship("EmployeeDependency", foreign_keys=[EmployeeDependency.dependent_employee_id], back_populates="dependent_employee")

class Qualification(db.Model):
    __tablename__ = 'qualifications'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    employees = relationship("EmployeeQualification", back_populates="qualification", cascade='all, delete-orphan')

class EmployeeQualification(db.Model):
    __tablename__ = 'employee_qualifications'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    qualification_id = Column(Integer, ForeignKey('qualifications.id'))

    employee = relationship("Employee", back_populates="qualifications")
    qualification = relationship("Qualification", back_populates="employees")

class Restriction(db.Model):
    __tablename__ = 'restrictions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    employees = relationship("EmployeeRestriction", back_populates="restriction", cascade='all, delete-orphan')

class EmployeeRestriction(db.Model):
    __tablename__ = 'employee_restrictions'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    restriction_id = Column(Integer, ForeignKey('restrictions.id'))
    value = Column(Integer)

    employee = relationship("Employee", back_populates="restrictions")
    restriction = relationship("Restriction", back_populates="employees")

class Driver(db.Model):
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)