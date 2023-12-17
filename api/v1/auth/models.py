from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, func


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TokenBlocklist(db.Model):  # type: ignore
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    type = Column(String(16), nullable=False)
    created_at = Column(
        DateTime, server_default=func.now(), nullable=False)
