from datetime import datetime
from sqlalchemy import extract
from api.error import InvalidAPIUsage
from ..models import DayOffRequest, Employee, DayOffRequestSchema
from ..validators import post_day_off_request_schema, put_day_off_request_schema
from .db_utils import session_scope, validate_data
from sqlalchemy.orm.session import Session as BaseSession


def get_all_requests_services(facility_id, year, month):
    with session_scope() as session:
        request = session.query(DayOffRequest).join(Employee).filter(
            extract('year', DayOffRequest.date) == year,
            extract('month', DayOffRequest.date) == month,
            Employee.facility_id == facility_id
        ).all()
        res = DayOffRequestSchema().dump(request, many=True)
        return res


def post_day_off_request_service(facility_id, employee_id, data):
    with session_scope() as session:
        validate_data(post_day_off_request_schema, data)
        has_request(employee_id, data['date'], session)
        new_request = DayOffRequest(
            employee_id=employee_id,
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            type_of_vacation=data['type_of_vacation']
        )
        session.add(new_request)
        session.flush()
        res = DayOffRequestSchema().dump(new_request)
        return res


def delete_request_service(employee_id, request_id):
    with session_scope() as session:
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id, request_id=request_id).first()
        if not request:
            return None
        session.delete(request)
        return request


def update_request_service(employee_id, request_id, data):
    with session_scope() as session:
        validate_data(put_day_off_request_schema, data)
        request = session.query(DayOffRequest).filter_by(employee_id=employee_id, request_id=request_id).first()
        if not request:
            return None
        request.type_of_vacation = data['type_of_vacation']
        request.updated_at = datetime.now()
        session.add(request)
        return DayOffRequestSchema().dump(request)


def has_request(employee_id, date, session: BaseSession):
    request = session.query(DayOffRequest).filter_by(employee_id=employee_id, date=date).first()
    if request:
        raise InvalidAPIUsage("The employee already has a request for this date", 400)
