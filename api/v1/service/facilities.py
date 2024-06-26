from flask import jsonify
from extensions import db_session
from ..validators import post_facility_schema, post_facility_atrubute_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint, Task
from api.error import InvalidAPIUsage
from .db_utils import session_scope, validate_data


def validate_and_create_facility_service(data):
    with session_scope() as session:
        validate_data(post_facility_schema, data)
        new_facility = Facility(**data)
        session.add(new_facility)
        res = FacilitySchema().dump(new_facility)
        return res


def delete_facility_service(facility_id):
    with session_scope() as session:
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            return None
        session.delete(facility)
        return facility


def get_facility_service(facility_id):
    with session_scope() as session:
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            return None
        return FacilitySchema().dump(facility)


def add_qualification_to_facility_service(facility_id, data):
    return add_attribute_to_facility(facility_id, data, Qualification, 'qualifications', 'qualification_id')


def delete_qualification_from_facility_service(facility_id, qualification_id):
    return delete_attribute_from_facility(facility_id, qualification_id, Qualification, 'qualifications', 'qualification_id')


def add_constraint_to_facility_service(facility_id, data):
    return add_attribute_to_facility(facility_id, data, Constraint, 'constraints', 'constraint_id')


def delete_constraint_from_facility_service(facility_id, constraint_id):
    return delete_attribute_from_facility(facility_id, constraint_id, Constraint, 'constraints', 'constraint_id')


def add_task_to_facility_service(facility_id, data):
    return add_attribute_to_facility(facility_id, data, Task, 'tasks', 'task_id')


def delete_task_from_facility_service(facility_id, task_id):
    return delete_attribute_from_facility(facility_id, task_id, Task, 'tasks', 'task_id')


def add_attribute_to_facility(facility_id, data, model_class, attribute_name, attribute_id):
    with session_scope() as session:
        validate_data(post_facility_atrubute_schema, data)
        attribute = session.query(model_class).filter(getattr(model_class, attribute_id) == data['id']).first()
        if not attribute:
            return None
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        getattr(facility, attribute_name).append(attribute)
        return FacilitySchema().dump(facility)


def delete_attribute_from_facility(facility_id, target_id, model_class, attribute_name, attribute_id):
    with session_scope() as session:
        facility = session.query(Facility).filter_by(facility_id=facility_id).first()
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        attribute = session.query(model_class).filter(getattr(model_class, attribute_id) == target_id).first()
        if not attribute:
            return False
        attribute_list = getattr(facility, attribute_name)
        if any(getattr(a, attribute_id) == target_id for a in attribute_list):
            attribute_list.remove(attribute)
            return jsonify({"message": f"{model_class.__name__} deleted successfully!"})
        else:
            raise InvalidAPIUsage(f"The facility does not have this {model_class.__name__}", 400)
