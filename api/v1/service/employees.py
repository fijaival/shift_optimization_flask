import logging
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
from extensions import db, jwt_required, self_facility_required
from sqlalchemy.exc import SQLAlchemyError


from api.error import InvalidAPIUsage
from ..validators import post_employee_schema, put_employee_schema
from ..models import Qualification, EmployeeConstraint, Constraint, Employee, Facility, EmployeeType, Dependency

from .utils import validate_data, get_instance_by_id, save_to_db, delete_from_db


def get_all_employees_service(facility_id):
    employees = Employee.query.filter_by(facility_id=facility_id).all()
    return employees


def add_employee_service(facility_id, data):
    validate_data(post_employee_schema, data)

    has_employee_type(data['employee_type_id'])
    has_constraint(facility_id, data['constraints'])
    has_qualification(facility_id, data['qualifications'])
    has_employee(facility_id, data["dependencies"])

    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        employee_type_id=data['employee_type_id'],
        facility_id=facility_id
    )
    for const_data in data['constraints']:
        found_cons = Constraint.query.filter_by(constraint_id=const_data["constraint_id"]).first()
        employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
        new_employee.employee_constraints.append(employee_constraint)
    for qual_data in data['qualifications']:
        found_qual = Qualification.query.filter_by(qualification_id=qual_data["qualification_id"]).first()
        new_employee.qualifications.append(found_qual)
    for dep_data in data['dependencies']:
        dependency = Dependency(dependent_employee_id=dep_data)
        new_employee.dependencies.append(dependency)

    save_to_db(new_employee)
    return new_employee


def delete_employee_service(employee_id):
    employee = get_instance_by_id(Employee, employee_id, "employee_id")
    if not employee:
        return None
    delete_from_db(employee)
    return employee


def update_employee_service(facility_id, employee_id, data):
    validate_data(put_employee_schema, data)

    employee = Employee.query.filter_by(employee_id=employee_id, facility_id=facility_id).first()
    if not employee:
        raise InvalidAPIUsage("Employee not found", 404)

    has_employee_type(data['employee_type_id'])
    has_constraint(facility_id, data['constraints'])
    has_qualification(facility_id, data['qualifications'])
    has_employee(facility_id, data["dependencies"])

    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.employee_type_id = data['employee_type_id']

    employee.employee_constraints.clear()
    for const_data in data['constraints']:
        found_cons = Constraint.query.filter_by(constraint_id=const_data["constraint_id"]).first()
        employee_constraint = EmployeeConstraint(constraint=found_cons, value=const_data["value"])
        employee.employee_constraints.append(employee_constraint)

    employee.qualifications.clear()
    for qual_data in data['qualifications']:
        found_qual = get_instance_by_id(Qualification, qual_data["qualification_id"], "qualification_id")
        employee.qualifications.append(found_qual)
    """
    #以下の依存関係の更新について
    depnedency.qualifications.clear()がデータベースに反映されないので、
    既存のものをcommitしてから依存関係を追加する
    """

    try:
        Dependency.query.filter_by(employee_id=employee_id).delete()
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise InvalidAPIUsage("Failed to clear dependencies", 400)

    for dep_data in data['dependencies']:
        dependency = Dependency(employee_id=employee_id, dependent_employee_id=dep_data)
        employee.dependencies.append(dependency)

    save_to_db(employee)
    return employee


def has_employee_type(employee_type_id):
    if not get_instance_by_id(EmployeeType, employee_type_id, "employee_type_id"):
        raise InvalidAPIUsage("Employee type not found", 404)


def has_constraint(facility_id, constraints):
    facility = get_instance_by_id(Facility, facility_id, "facility_id")
    for q in constraints:
        constraint = get_instance_by_id(Constraint, q["constraint_id"], "constraint_id")
        if not constraint:
            raise InvalidAPIUsage("Constraint not found", 404)
        if not any(con.constraint_id == q["constraint_id"] for con in facility.constraints):
            raise InvalidAPIUsage("This facility does not have the constraint with ID" +
                                  f"{q['constraint_id']} registered.", 404)


def has_qualification(facility_id, qualifications):
    facility = get_instance_by_id(Facility, facility_id, "facility_id")
    for q in qualifications:
        qualification = get_instance_by_id(Qualification, q["qualification_id"], "qualification_id")
        if not qualification:
            raise InvalidAPIUsage("Qualification not found", 404)
        if not any(qual.qualification_id == q["qualification_id"] for qual in facility.qualifications):
            raise InvalidAPIUsage(f"This facility does not have the qualification with ID {
                                  q['qualification_id']} registered.", 404)


def has_employee(facility_id, dependencies):
    for d in dependencies:
        employee = Employee.query.filter_by(employee_id=d, facility_id=facility_id).first()
        if not employee:
            raise InvalidAPIUsage("dependency not found", 404)
