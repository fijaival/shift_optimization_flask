from extensions import db
from api.error import InvalidAPIUsage
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def validate_data(schema, data):
    error = schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)


def get_instance_by_id(model, id, id_field):
    instance = model.query.filter_by(**{id_field: id}).first()
    if not instance:
        return None
    return instance


def save_to_db(instance):
    try:
        db.session.add(instance)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise InvalidAPIUsage(f"An error occurred: {str(e)}", 500)


def delete_from_db(instance):
    try:
        db.session.delete(instance)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
        # raise InvalidAPIUsage("Cannot delete due to external constraints.", 400)
    except SQLAlchemyError as e:
        db.session.rollback()
        raise InvalidAPIUsage(f"An error occurred while deleting: {str(e)}", 500)
