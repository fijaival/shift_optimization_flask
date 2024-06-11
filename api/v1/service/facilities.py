from extensions import db
from ..validators import post_facility_schema, post_qualification_schema, post_constraint_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint
from api.error import InvalidAPIUsage

from .utils import validate_data, get_instance_by_id, save_to_db, delete_from_db


def validate_and_create_facility_service(data):
    validate_data(post_facility_schema, data)
    new_facility = Facility(**data)
    save_to_db(new_facility)
    return FacilitySchema().dump(new_facility)


def delete_facility_service(facility_id):
    facility = get_instance_by_id(Facility, facility_id, 'facility_id')
    if not facility:
        return None
    delete_from_db(facility)
    return facility


def get_facility_service(facility_id):
    facility = get_instance_by_id(Facility, facility_id, 'facility_id')
    if not facility:
        return None
    return FacilitySchema().dump(facility)


def add_qualification_to_facility_service(facility_id, data):
    validate_data(post_qualification_schema, data)
    qualification = Qualification.query.filter_by(name=data['name']).first()
    if not qualification:
        qualification = Qualification(**data)
        save_to_db(qualification)
    facility = get_instance_by_id(Facility, facility_id, 'facility_id')
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    if any(q.name == data['name'] for q in facility.qualifications):
        raise InvalidAPIUsage("The facility already has its qualification", 400)
    facility.qualifications.append(qualification)
    db.session.commit()
    return FacilitySchema().dump(facility)


def delete_qualification_from_facility_service(facility_id, qualification_id):
    facility = get_instance_by_id(Facility, facility_id, 'facility_id')
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    qualification = Qualification.query.filter_by(qualification_id=qualification_id).first()
    if not qualification:
        raise InvalidAPIUsage("Qualification not found", 404)
    if any(q.qualification_id == qualification_id for q in facility.qualifications):
        facility.qualifications.remove(qualification)
        db.session.commit()
        return True
    raise InvalidAPIUsage("The facility does not have this qualification", 400)


def add_constraint_to_facility_service(facility_id, data):
    validate_data(post_constraint_schema, data)
    constraint = Constraint.query.filter_by(name=data['name']).first()
    if not constraint:
        constraint = Constraint(**data)
        save_to_db(constraint)
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    if any(q.name == data['name'] for q in facility.constraints):
        raise InvalidAPIUsage("The facility already has its constraint", 400)
    facility.constraints.append(constraint)
    db.session.commit()
    return FacilitySchema().dump(facility)


def delete_constraint_from_facility_service(facility_id, constraint_id):
    facility = get_instance_by_id(Facility, facility_id, 'facility_id')
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    constraint = get_instance_by_id(Constraint, constraint_id, 'constraint_id')
    if not constraint:
        raise InvalidAPIUsage("Constraint not found", 404)
    if any(q.constraint_id == constraint_id for q in facility.constraints):
        facility.constraints.remove(constraint)
        db.session.commit()
        return True
    raise InvalidAPIUsage("The facility does not have this constraint", 400)
