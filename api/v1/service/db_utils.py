from api.error import InvalidAPIUsage
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from extensions import db_session
from contextlib import contextmanager


def validate_data(schema, data):
    error = schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)


def get_instance_by_id(model, id, id_field, session):
    instance = session.query(model).filter_by(**{id_field: id}).first()
    if not instance:
        return None
    return instance


def save_to_db(instance, session):
    try:
        session.add(instance)
        session.commit()
    except IntegrityError as sqlalchemy_error:
        session.rollback()
        raise sqlalchemy_error


def delete_from_db(instance, session):
    try:
        session.delete(instance)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    except SQLAlchemyError as e:
        session.rollback()
        raise InvalidAPIUsage(f"An error occurred while deleting: {str(e)}", 500)


@contextmanager
def session_scope():
    session = db_session()  # def __enter__
    try:
        yield session  # with asでsessionを渡す
        session.commit()  # 何も起こらなければcommit()
    except IntegrityError as e:
        print(e)
        print(e.orig)
        session.rollback()  # errorが起こればrollback()
        if 'Duplicate' in str(e.orig):
            raise InvalidAPIUsage("An error ocurred due to duplicate data", 400)
        elif 'cannot be null' in str(e.orig):
            raise InvalidAPIUsage("An error occurred due to foreign key constraints", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the instance", 500)
    finally:
        session.close()  # どちらにせよ最終的にはclose()
