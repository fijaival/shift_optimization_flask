from extensions import Base, ma
from datetime import datetime


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Constraint(Base):
    __tablename__ = 'constraints'

    constraint_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class ConstraintSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Constraint
