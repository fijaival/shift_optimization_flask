import os
import pytest
from api import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from extensions import Base


from extensions import Base
from dotenv import load_dotenv

# テスト用の.envファイルを読み込む
load_dotenv('.env.test', override=True)


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def engine():
    TEST_DATABASE_URL = 'mysql+pymysql://{user}:{password}@{host}:{PORT}/{db_name}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host':     os.getenv('DB_HOST'),
        'PORT':    os.getenv('DB_PORT'),
        'db_name': os.getenv('DB_NAME'),
    })
    print(TEST_DATABASE_URL)
    return create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def setup_db(connection):
    Base.metadata.create_all(bind=connection)
    yield
    Base.metadata.drop_all(bind=connection)


@pytest.fixture(scope="function")
def session(connection, setup_db):
    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)
    session = Session()

    yield session

    session.close()


@contextmanager
def mock_session_scope(session):
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
