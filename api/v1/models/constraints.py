from extensions import db, ma
from datetime import datetime


from sqlalchemy import Column, Integer, String, DateTime


class Constraint(db.Model):
    __tablename__ = 'constraints'

    constraint_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)


class ConstraintSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Constraint
