from api.error import InvalidAPIUsage
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


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
