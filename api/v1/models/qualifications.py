from extensions import Base, ma
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Qualification(Base):
    __tablename__ = 'qualifications'

    qualification_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class QualificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Qualification
