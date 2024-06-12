from datetime import datetime
from flask import request, jsonify
from sqlalchemy import extract
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from api.error import InvalidAPIUsage
from ..models.day_off_requests import DayOffRequest
from ..validators import post_day_off_request_schema
from .utils import validate_data, get_instance_by_id, save_to_db, delete_from_db


def get_all_requests_services(facility_id, year, month):
    requests = DayOffRequest.query.filter(
        extract('year', DayOffRequest.date) == year,
        extract('month', DayOffRequest.date) == month,
        DayOffRequest.facility_id == facility_id
    ).all()
    pass


def post_day_off_request_service(facility_id, employee_id, data):
    try:
        validate_data(post_day_off_request_schema, data)
        has_request(employee_id, data['date'])
        new_request = DayOffRequest(
            employee_id=employee_id,
            date=data['date'],
            type_of_vacation=data['type_of_vacation']
        )
        save_to_db(new_request)
        return new_request
    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e.orig):
            raise InvalidAPIUsage("The employee already has a request for this date", 400)
        elif 'foreign key constraint' in str(e.orig):
            raise InvalidAPIUsage("The employee does not exist", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the request", 500)


def has_request(employee_id, date):
    request = DayOffRequest.query.filter_by(employee_id=employee_id, date=date).first()
    if request:
        raise InvalidAPIUsage("The employee already has a request for this date", 400)
