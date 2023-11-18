class Config:
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///order.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False