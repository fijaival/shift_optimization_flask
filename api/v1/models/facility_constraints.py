from datetime import datetime
from extensions import db, ma
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship


class FacilityConstraint(db.Models):
    __tablename__ = 'facility_constraints'
    facility_constraint_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey(
        'facilities.facility_id'), nullable=False)
    constraint_id = Column(Integer, ForeignKey(
        'constraints.constraint_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    facility = relationship('Facility', back_populates='facility_constraints')
    constraint = relationship(
        'Constraint', back_populates='facility_constraints')
    __table_args__ = (
        UniqueConstraint('facility_id', 'constraint_id',
                         name='uq_facility_constraint'),
    )
