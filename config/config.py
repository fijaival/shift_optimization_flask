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
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=24)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///order.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
