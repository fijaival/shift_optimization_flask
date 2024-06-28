from ..validators import post_shifts_schema
from sqlalchemy import extract
from ..models import Shift, ShiftSchema, Employee
from ..utils.context_maneger import session_scope
from ..utils.validate import validate_data


def post_shifts_service(data):
    with session_scope() as session:
        shifts = data["shifts"]
        validate_data(post_shifts_schema, shifts)
        for item in shifts:
            new_shift = Shift(**item)
            session.add(new_shift)


def get_shifts_service(facility_id, year, month):
    with session_scope() as session:
        employee = session.query(Employee).filter_by(facility_id=facility_id).all()
        if not employee:
            return None
        employee_ids = [emp.employee_id for emp in employee]
        shifts = session.query(Shift).filter(
            extract('year', Shift.date) == year,
            extract('month', Shift.date) == month,
            Shift.employee_id.in_(employee_ids)
        ).all()
        res = ShiftSchema().dump(shifts, many=True)
        return res
