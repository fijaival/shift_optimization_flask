from extensions import db
from datetime import datetime


from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Dependency(db.Model):
    __tablename__ = 'dependencies'

    dependency_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    dependent_employee_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    employee = relationship('Employee', foreign_keys=[
                            employee_id], back_populates='dependencies')
    dependent_employee = relationship('Employee', foreign_keys=[
                                      dependent_employee_id], back_populates='dependent_employees')

    __table_args__ = (
        UniqueConstraint('employee_id', 'dependent_employee_id',
                         name='uq_dependency'),
    )
