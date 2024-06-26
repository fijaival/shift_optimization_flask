from extensions import Base, ma
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
    created_at = ma.auto_field(load_only=True)
    updated_at = ma.auto_field(load_only=True)
