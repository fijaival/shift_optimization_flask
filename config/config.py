from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_LEEWAY = 0
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # In production, this should likely be True
    JWT_ACCESS_COOKIE_PATH = '/api/v1/'
    JWT_REFRESH_COOKIE_PATH = '/api/v1/'
    JWT_CSRF_IN_COOKIES = False

    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///order.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
