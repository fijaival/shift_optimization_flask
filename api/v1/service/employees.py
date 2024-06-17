import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import scoped_session
from extensions import Base, db_session, jwt_required, self_facility_required
from api.error import InvalidAPIUsage
from ..validators import post_employee_schema, put_employee_schema
from ..models import Qualification, EmployeeConstraint, Constraint, Employee, Facility, EmployeeType, Dependency, EmployeeSchema
from .utils import validate_data, get_instance_by_id, save_to_db, delete_from_db


def get_all_employees_service(facility_id):
    session = db_session()
    employees = session.query(Employee).filter_by(facility_id=facility_id).all()
    return employees


def add_employee_service(facility_id, data):
    session = db_session()
    try:
        validate_data(post_employee_schema, data)
        has_employee_type(data['employee_type_id'], session)
        has_constraint(facility_id, data['constraints'], session)
        has_qualification(facility_id, data['qualifications'], session)
        has_employee(facility_id, data["dependencies"], session)

        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            employee_type_id=data['employee_type_id'],
            facility_id=facility_id
        )
        for const_data in data['constraints']:
            found_cons = get_instance_by_id(Constraint, const_data["constraint_id"], "constraint_id", session)
            employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
            new_employee.employee_constraints.append(employee_constraint)
        for qual_data in data['qualifications']:
            found_qual = get_instance_by_id(Qualification, qual_data["qualification_id"], "qualification_id", session)
            new_employee.qualifications.append(found_qual)
        for dep_data in data['dependencies']:
            dependency = Dependency(dependent_employee_id=dep_data)
            new_employee.dependencies.append(dependency)

        save_to_db(new_employee, session)
        res = EmployeeSchema().dump(new_employee)
        return res
    except IntegrityError:
        session.rollback()
        raise InvalidAPIUsage("An error occurred while saving the employee", 500)
    except SQLAlchemyError:
        session.rollback()
        raise InvalidAPIUsage("An unexpected error occurred", 500)
    finally:
        session.close()


def delete_employee_service(employee_id):
    session = db_session()
    try:
        employee = get_instance_by_id(Employee, employee_id, "employee_id", session)
        if not employee:
            return None
        delete_from_db(employee, session)
        return employee
    finally:
        session.close()


def update_employee_service(facility_id, employee_id, data):
    session = db_session()
    try:
        validate_data(put_employee_schema, data)
        employee = session.query(Employee).filter_by(employee_id=employee_id, facility_id=facility_id).first()
        if not employee:
            raise InvalidAPIUsage("Employee not found", 404)

        has_employee_type(data['employee_type_id'], session)
        has_constraint(facility_id, data['constraints'], session)
        has_qualification(facility_id, data['qualifications'], session)
        has_employee(facility_id, data["dependencies"], session)

        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        employee.employee_type_id = data['employee_type_id']

        employee.employee_constraints.clear()
        for const_data in data['constraints']:
            found_cons = get_instance_by_id(Constraint, const_data["constraint_id"], "constraint_id", session)
            employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
            employee.employee_constraints.append(employee_constraint)

        employee.qualifications.clear()
        for qual_data in data['qualifications']:
            found_qual = get_instance_by_id(Qualification, qual_data["qualification_id"], "qualification_id", session)
            employee.qualifications.append(found_qual)

        session.query(Dependency).filter_by(employee_id=employee_id).delete()
        for dep_data in data['dependencies']:
            dependency = Dependency(employee_id=employee_id, dependent_employee_id=dep_data)
            employee.dependencies.append(dependency)

        save_to_db(employee, session)
        res = EmployeeSchema().dump(employee)
        return res
    except IntegrityError:
        session.rollback()
        raise InvalidAPIUsage("An error occurred while saving the employee", 500)
    finally:
        session.close()


def has_employee_type(employee_type_id, session):
    if not get_instance_by_id(EmployeeType, employee_type_id, "employee_type_id", session):
        raise InvalidAPIUsage("Employee type not found", 404)


def has_constraint(facility_id, constraints, session):
    facility = get_instance_by_id(Facility, facility_id, "facility_id", session)
    for q in constraints:
        constraint = get_instance_by_id(Constraint, q["constraint_id"], "constraint_id", session)
        if not constraint:
            raise InvalidAPIUsage("Constraint not found", 404)
        if not any(con.constraint_id == q["constraint_id"] for con in facility.constraints):
            raise InvalidAPIUsage("This facility does not have the constraint with ID" +
                                  f"{q['constraint_id']} registered.", 404)


def has_qualification(facility_id, qualifications, session):
    facility = get_instance_by_id(Facility, facility_id, "facility_id", session)
    for q in qualifications:
        qualification = get_instance_by_id(Qualification, q["qualification_id"], "qualification_id", session)
        if not qualification:
            raise InvalidAPIUsage("Qualification not found", 404)
        if not any(qual.qualification_id == q["qualification_id"] for qual in facility.qualifications):
            raise InvalidAPIUsage("This facility does not have the qualification with ID" +
                                  f"{q['qualification_id']} registered.", 404)


def has_employee(facility_id, dependencies, session):
    for d in dependencies:
        employee = session.query(Employee).filter_by(employee_id=d, facility_id=facility_id).first()
        if not employee:
            raise InvalidAPIUsage("dependency not found", 404)
