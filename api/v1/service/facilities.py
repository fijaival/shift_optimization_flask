from extensions import db_session
from ..validators import post_facility_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint, Task
from api.error import InvalidAPIUsage
from sqlalchemy.exc import IntegrityError

from .db_utils import validate_data, get_instance_by_id, save_to_db, delete_from_db


def validate_and_create_facility_service(data):
    session = db_session()
    try:
        validate_data(post_facility_schema, data)
        new_facility = Facility(**data)
        save_to_db(new_facility, session)
        return FacilitySchema().dump(new_facility)
    except IntegrityError as e:
        session.rollback()
        raise InvalidAPIUsage("An error occurred while saving the facility", 500)
    finally:
        session.close()


def delete_facility_service(facility_id):
    session = db_session()
    try:
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            return None
        delete_from_db(facility, session)
        return facility
    finally:
        session.close()


def get_facility_service(facility_id):
    session = db_session()
    try:
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            return None
        return FacilitySchema().dump(facility)
    finally:
        session.close()


def add_qualification_to_facility_service(facility_id, data):
    session = db_session()
    try:
        validate_data(post_facility_schema, data)
        qualification = session.query(Qualification).filter_by(name=data['name']).first()
        if not qualification:
            qualification = Qualification(**data)
            session.add(qualification)
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        facility.qualifications.append(qualification)
        session.commit()
        return FacilitySchema().dump(facility)
    except IntegrityError as e:
        session.rollback()
        if 'Duplicate' in str(e.orig):
            raise InvalidAPIUsage("The facility already has this qualification", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the qualification", 500)
    finally:
        session.close()


def delete_qualification_from_facility_service(facility_id, qualification_id):
    session = db_session()
    try:
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        qualification = get_instance_by_id(Qualification, qualification_id, 'qualification_id', session)
        if not qualification:
            raise InvalidAPIUsage("Qualification not found", 404)
        if any(q.qualification_id == qualification_id for q in facility.qualifications):
            facility.qualifications.remove(qualification)
            session.commit()
            return True
        raise InvalidAPIUsage("The facility does not have this qualification", 400)
    finally:
        session.close()


def add_constraint_to_facility_service(facility_id, data):
    session = db_session()
    try:
        validate_data(post_facility_schema, data)
        constraint = session.query(Constraint).filter_by(name=data['name']).first()
        if not constraint:
            constraint = Constraint(**data)
            session.add(constraint)
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        facility.constraints.append(constraint)
        session.commit()
        return FacilitySchema().dump(facility)
    except IntegrityError as e:
        print(e.orig)
        if 'Duplicate' in str(e.orig):
            raise InvalidAPIUsage("The facility already has its constraint", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the constraint", 500)
    finally:
        session.close()


def delete_constraint_from_facility_service(facility_id, constraint_id):
    session = db_session()
    try:
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        constraint = get_instance_by_id(Constraint, constraint_id, 'constraint_id', session)
        if not constraint:
            raise InvalidAPIUsage("Constraint not found", 404)
        if any(q.constraint_id == constraint_id for q in facility.constraints):
            facility.constraints.remove(constraint)
            session.commit()
            return True
        raise InvalidAPIUsage("The facility does not have this constraint", 400)
    finally:
        session.close()


def add_task_to_facility_service(facility_id, data):
    session = db_session()
    try:
        validate_data(post_facility_schema, data)
        task = session.query(Task).filter_by(name=data['name']).first()
        if not task:
            task = Task(**data)
            session.add(task)
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        facility.tasks.append(task)
        session.commit()
        return FacilitySchema().dump(facility)
    except IntegrityError as e:
        print(e.orig)
        if 'Duplicate' in str(e.orig):
            raise InvalidAPIUsage("The facility already has this task", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the task", 500)
    finally:
        session.close()


def delete_task_from_facility_service(facility_id, task_id):
    session = db_session()
    try:
        facility = get_instance_by_id(Facility, facility_id, 'facility_id', session)
        if not facility:
            raise InvalidAPIUsage("Facility not found", 404)
        task = get_instance_by_id(Task, task_id, 'task_id', session)
        if not task:
            raise InvalidAPIUsage("Task not found", 404)
        if any(q.task_id == task_id for q in facility.tasks):
            facility.tasks.remove(task)
            session.commit()
            return True
        raise InvalidAPIUsage("The facility does not have this task", 400)
    finally:
        session.close()
