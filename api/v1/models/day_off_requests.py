from extensions import Base, ma, fields
from datetime import datetime
from datetime import date as dt_date
from sqlalchemy import String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column


class DayOffRequest(Base):
    __tablename__ = 'day_off_requests'

    request_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.employee_id', ondelete="CASCADE"), nullable=False)
    date: Mapped[dt_date] = mapped_column(Date, nullable=False)
    type_of_vacation: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_day_off_request'),
    )


class DayOffRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DayOffRequest
    employee = fields.Nested('EmployeeSchema', only=('employee_id', 'first_name', 'last_name'))
