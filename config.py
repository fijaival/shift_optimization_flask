from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()


class Config:
    # httplonlyはデフォルトでTrue
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_SECURE = True  # In production, this should likely be True
    JWT_ACCESS_COOKIE_PATH = '/v1/'
    JWT_REFRESH_COOKIE_PATH = '/v1/'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{PORT}/{db_name}?charset=utf8'.format(**{
        'user': 'ope1',
        'password': 'ope1',
        'host': 'localhost',
        'PORT': "3306",
        'db_name': 'shiftOptimization'
    })
