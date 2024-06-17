from datetime import datetime
from flask import request, jsonify
from sqlalchemy import extract
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from extensions import db_session
from api.error import InvalidAPIUsage
from ..models import DayOffRequest, Employee, DayOffRequestSchema
from ..validators import post_day_off_request_schema
from .utils import validate_data, save_to_db, delete_from_db


def get_all_requests_services(facility_id, year, month):
    session = db_session()
    try:
        request = session.query(DayOffRequest).join(Employee).filter(
            extract('year', DayOffRequest.date) == year,
            extract('month', DayOffRequest.date) == month,
            Employee.facility_id == facility_id
        ).all()
        res = DayOffRequestSchema().dump(request, many=True)
        return res
    except SQLAlchemyError:
        raise InvalidAPIUsage("An error occurred while getting the requests", 500)


def post_day_off_request_service(facility_id, employee_id, data):
    sesion = db_session()
    try:
        validate_data(post_day_off_request_schema, data)
        has_request(employee_id, data['date'], sesion)
        new_request = DayOffRequest(
            employee_id=employee_id,
            date=data['date'],
            type_of_vacation=data['type_of_vacation']
        )
        save_to_db(new_request, sesion)
        res = DayOffRequestSchema().dump(new_request)
        return res
    except IntegrityError as e:
        sesion.rollback()
        if 'duplicate key value violates unique constraint' in str(e.orig):
            raise InvalidAPIUsage("The employee already has a request for this date", 400)
        elif 'foreign key constraint' in str(e.orig):
            raise InvalidAPIUsage("The employee does not exist", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the request", 500)
    finally:
        sesion.close()


def delete_request_service(employee_id, request_id):
    session = db_session()
    try:
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id, request_id=request_id).first()
        if not request:
            return None
        delete_from_db(request, session)
        return request
    finally:
        session.close()


def update_request_service(employee_id, request_id, data):
    session = db_session()
    try:
        validate_data(post_day_off_request_schema, data)
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id,
                                                         request_id=request_id, date=data["date"]).first()
        if not request:
            raise InvalidAPIUsage("The request does not exist", 404)
        request.type_of_vacation = data['type_of_vacation']
        save_to_db(request, session)
        res = DayOffRequestSchema().dump(request)
        return res
    except IntegrityError:
        session.rollback()
        raise InvalidAPIUsage("An error occurred while saving the employee", 500)
    finally:
        session.close()


def has_request(employee_id, date, session):
    request = session.query(DayOffRequest).filter_by(employee_id=employee_id, date=date).first()
    if request:
        raise InvalidAPIUsage("The employee already has a request for this date", 400)
