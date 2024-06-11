from sqlalchemy import select
from extensions import db, jwt_required, self_facility_required
from sqlalchemy.exc import SQLAlchemyError


from api.error import InvalidAPIUsage
from ..validators import post_employee_schema, put_employee_schema
from ..models import Qualification, EmployeeConstraint, Constraint, Employee, Facility, EmployeeType
from ..models import facility_qualifications, facility_constraints


def get_all_employees_service(facility_id):
    employees = Employee.query.filter_by(facility_id=facility_id).all()
    return employees


def add_employee_service(facility_id, data):
    error = post_employee_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)

    has_employee_type(data['employee_type_id'])
    has_constraint(facility_id, data['constraints'])
    has_qualification(facility_id, data['qualifications'])

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
    db.session.add(new_employee)
    db.session.commit()
    return new_employee


def delete_employee_service(employee_id):
    try:
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        if not employee:
            return None

        db.session.delete(employee)
        db.session.commit()
        return employee
    except SQLAlchemyError:
        db.session.rollback()
        raise


def update_employee_service(facility_id, employee_id, data):
    error = put_employee_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)

    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        raise InvalidAPIUsage("Employee not found", 404)

    has_employee_type(data['employee_type_id'])
    has_constraint(facility_id, data['constraints'])
    has_qualification(facility_id, data['qualifications'])

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
        found_qual = Qualification.query.filter_by(qualification_id=qual_data["qualification_id"]).first()
        employee.qualifications.append(found_qual)
    db.session.commit()


def has_employee_type(employee_type_id):
    has_employee_type = EmployeeType.query.filter_by(employee_type_id=employee_type_id).first()
    if not has_employee_type:
        raise InvalidAPIUsage("Employee type not found", 404)


def has_constraint(facility_id, constraints):
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    for q in constraints:
        constraint = Constraint.query.filter_by(constraint_id=q["constraint_id"]).first()
        if not constraint:
            raise InvalidAPIUsage("Constraint not found", 404)
        has_cons = any(con.constraint_id == q["constraint_id"] for con in facility.constraints)
        for con in facility.constraints:
            print(con.constraint_id)
        if not has_cons:
            raise InvalidAPIUsage("This facility does not have the constraint with ID " +
                                  f"{q["constraint_id"]} registered.", 404)


def has_qualification(facility_id, qualifications):
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    for q in qualifications:
        qualification = Qualification.query.filter_by(qualification_id=q["qualification_id"]).first()
        if not qualification:
            raise InvalidAPIUsage("Qualification not found", 404)
        has_qual = any(qual.qualification_id == q["qualification_id"] for qual in facility.qualifications)
        if not has_qual:
            raise InvalidAPIUsage("This facility does not have the qualification with ID " +
                                  f"{q["qualification_id"]} registered.", 404)
