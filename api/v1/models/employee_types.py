from extensions import db, ma
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column


class EmployeeType(db.Model):
    __tablename__ = 'employee_types'

    employee_type_id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class EmployeeTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeType
    created_at = ma.auto_field(load_only=True)
    updated_at = ma.auto_field(load_only=True)
