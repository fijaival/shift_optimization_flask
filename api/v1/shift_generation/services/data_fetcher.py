# データ取得関数は再定義（不要な情報は取得しない）
from extensions import db
from ...employees import Employee, employees_schema
from ...drivers import Driver, drivers_schema
from ...shifts_requests import ShiftRequest, shift_request_schema
from ...drivers_requests import DriversRequests, drivers_request_schema
from ...dependencies import EmployeeDependency, employee_dependency_schema
from ...shifts import Shift, shifts_schema
from ...qualifications import Qualification, qualification_schema
from ...employee_qualifications import EmployeeQualification, employee_qualification_schema
from ...employee_restrictions import EmployeeRestriction, employee_restriction_schema
from ...restrictions import Restriction, restriction_schema


from flask import Blueprint, jsonify, request
from sqlalchemy import extract

# employee


def fetch_all_employees():
    data = Employee.query.all()
    return jsonify(employees_schema.dump(data))

# drivers


def fetch_all_drivers():
    data = Driver.query.all()
    return jsonify(drivers_schema.dump(data, many=True))

# shifts_requests


def fetch_shift_requests_for_month(year, month):
    # 指定された年と月のシフト希望を取得
    shift_requests = ShiftRequest.query.filter(
        extract('year', ShiftRequest.date) == year,
        extract('month', ShiftRequest.date) == month
    ).all()

    # シフト希望データのシリアライズ（または適切な形式への変換）が必要
    return jsonify(shift_request_schema.dump(
        shift_requests, many=True))

# drivers_requests


def fetch_drivers_requests_for_month(year, month):
    shift_requests = DriversRequests.query.filter(
        extract('year', DriversRequests.date) == year,
        extract('month', DriversRequests.date) == month
    ).all()
    return jsonify(drivers_request_schema.dump(
        shift_requests, many=True))


# qualificationsとemployees_qualifications
def fetch_qualifications():
    results = db.session.query(
        Qualification.name,
        EmployeeQualification.employee_id
    ).join(
        EmployeeQualification,
        Qualification.id == EmployeeQualification.qualification_id
    ).all()
    data = []
    for qualification_name, employee_id in results:
        combined_data = {
            'qualification_name': qualification_name,
            'employee_id': employee_id
        }
        data.append(combined_data)
    return jsonify(data)


# restrictionsとemployees_restrictions
def fetch_restrictions():
    results = db.session.query(
        Restriction.name,
        EmployeeRestriction.employee_id,
        EmployeeRestriction.value
    ).join(
        EmployeeRestriction,
        Restriction.id == EmployeeRestriction.restriction_id
    ).all()

    data = []
    for restriction_name, employee_id, value in results:
        restriction_data = {
            'restriction_name': restriction_name,
            'employee_id': employee_id,
            'value': value
        }
        data.append(restriction_data)

    return jsonify(data)
# employees_dependencies


def fetch_all_dependencies():
    data = EmployeeDependency.query.all()
    return jsonify(employee_dependency_schema.dump(data, many=True))

# shifts(last month)


def fetch_shifts_for_month(year, month):
    shifts = Shift.query.filter(
        extract('year', Shift.date) == year,
        extract('month', Shift.date) == month
    ).all()
    return jsonify(shifts_schema.dump(shifts))
