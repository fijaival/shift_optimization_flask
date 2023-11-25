# データ取得関数は再定義（不要な情報は取得しない）
from sqlalchemy.orm import joinedload
from extensions import db
from ...employees import Employee
from ...drivers import Driver
from ...shifts_requests import ShiftRequest
from ...drivers_requests import DriversRequests
from ...shifts import Shift

import calendar
from flask import jsonify
from sqlalchemy import extract
from datetime import date


def fetch_all_employees_details(year, month):
    # joinedload を使用して関連データを一括で取得
    employees = db.session.query(Employee).options(
        joinedload(Employee.qualifications),
        joinedload(Employee.restrictions),
        joinedload(Employee.dependencies),
    ).all()
    last_month = month - 1

    # 月末の7日間の範囲を設定
    last_day = calendar.monthrange(year, last_month)[1]
    start_date = date(year, last_month, last_day - 6)
    end_date = date(year, last_month, last_day)

    all_employees_data = []

    for employee in employees:

        shift_requests = ShiftRequest.query.filter(
            ShiftRequest.employee_id == employee.id,
            extract('year', ShiftRequest.date) == year,
            extract('month', ShiftRequest.date) == month
        ).all()

        last_month_shifts = Shift.query.filter(
            Shift.employee_id == employee.id,
            extract('year', Shift.date) == year,
            extract('month', Shift.date) == last_month,
            Shift.date.between(start_date, end_date)
        ).all()

        # 従業員の基本情報
        employee_data = {
            "id": employee.id,
            "name": employee.last_name + employee.first_name,
            "qualifications": [q.qualification.name for q in employee.qualifications],
            "restrictions": [{
                "name": r.restriction.name,
                "value": r.value}
                for r in employee.restrictions
            ],
            "dependencies": [d.required_employee_id for d in employee.dependencies],
            "last_month_shifts": [s.type_of_work for s in last_month_shifts],
            "shift_requests": [request.date.day for request in shift_requests],
            "paid": [request.date.day for request in shift_requests if request.type_of_vacation == "有"]

        }

        all_employees_data.append(employee_data)

    return all_employees_data


def fetch_all_drivers_details(year, month):
    drivers = db.session.query(Driver).all()
    year = 2023
    month = 11

    all_drivers_data = []

    for driver in drivers:
        shift_requests = DriversRequests.query.filter(
            DriversRequests.driver_id == driver.id,
            extract('year', DriversRequests.date) == year,
            extract('month', DriversRequests.date) == month
        ).all()

        driver_data = {
            "id": driver.id,
            "name": driver.last_name + driver.first_name,
            "driver_requests": [request.date.day for request in shift_requests],
            "paid": [request.date.day for request in shift_requests if request.type_of_vacation == "有"]
        }

        all_drivers_data.append(driver_data)

    return all_drivers_data
