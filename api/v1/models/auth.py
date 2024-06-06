from datetime import datetime
from extensions import db, ma, fields

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
# from .facilities import Facility


class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey(
        'facilities.facility_id'), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)

    def __init__(self, facility_id, username, password, is_admin=0):
        self.facility_id = facility_id
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    password_hash = ma.auto_field(load_only=True)
    facility = fields.Nested('FacilitySchema', only=(
        'facility_id', 'facility_name'))


class TokenBlocklist(db.Model):  # type: ignore
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
