from datetime import datetime
from extensions import db, ma
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship


class FacilityQualifications(db.Model):
    __tablename__ = 'facility_qualifications'
    facility_qualification_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey(
        'facilities.facility_id'), nullable=False)
    qualification_id = Column(Integer, ForeignKey(
        'qualifications.qualification_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    facility = relationship(
        'Facility', back_populates='facility_qualifications')
    qualification = relationship(
        'Qualification', back_populates='facility_qualifications')
    __table_args__ = (
        UniqueConstraint('facility_id', 'qualification_id',
                         name='uq_facility_qualification'),
    )
