from extensions import db, jwt_required, self_facility_required
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select
from flask import Blueprint, jsonify, request
from ..models import Employee, EmployeeSchema, facility_constraints, facility_qualifications
from ..validators import post_employee_schema
from api.error import InvalidAPIUsage

from ..service.employees import get_all_employees_service, add_employee_service, delete_employee_service, update_employee_service

#############
from ..models.qualifications import Qualification
from ..models import Constraint
from ..models.dependencies import Dependency


from ..schemas import employee_schema, employees_schema
# from ..models.employee_qualifications import EmployeeQualification
# from ..models.employee_constraints import EmployeeConstraint

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/facilities/<int:facility_id>/employees', methods=["GET"])
@self_facility_required
def get_employee(facility_id):
    """Get all employees in a facility."""
    employees = get_all_employees_service(facility_id)

    if not employees:
        raise InvalidAPIUsage("No employees found", 404)
    res = EmployeeSchema().dump(employees, many=True)
    return res, 200


@employees_bp.route('/facilities/<int:facility_id>/employees', methods=["POST"])
@self_facility_required
def add_employee(facility_id):
    "add employee to facility"
    data = request.json
    new_employee = add_employee_service(facility_id, data)
    res = EmployeeSchema().dump(new_employee)
    return res, 201


@employees_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>', methods=["DELETE"])
@self_facility_required
def delete_employee(facility_id, employee_id):
    "delete employee from facility"
    try:
        employee = delete_employee_service(employee_id)
        if not employee:
            raise InvalidAPIUsage("Employee not found", 404)
        return jsonify({"message": "Employee deleted successfully!"}), 200
    except InvalidAPIUsage as e:
        raise e
    except SQLAlchemyError as e:
        db.session.rollback()
        raise InvalidAPIUsage("An error occurred while deleting the employee", 500)


@employees_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>', methods=["PUT"])
@self_facility_required
def update_employee(facility_id, employee_id):
    "update employee information"
    data = request.json
    updated_employee = update_employee_service(facility_id, employee_id, data)
    res = EmployeeSchema().dump(updated_employee)
    return res, 201

    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        raise InvalidAPIUsage("Employee not found", 404)
    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.employee_type_id = data['employee_type_id']
    db.session.commit()
    return jsonify({"message": "Employee updated successfully!"}), 200
