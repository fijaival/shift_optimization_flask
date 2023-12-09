from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_LEEWAY = 0
    JWT_EXPIRATION_DELTA = timedelta(seconds=300)
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///order.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
