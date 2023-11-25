from .services.models import Employee, Driver
from .services.data_fetcher import fetch_all_employees_details, fetch_all_drivers_details
from .services.shift_scheduler import ShiftScheduler
import calendar


def optimize(year, month, holiday_set):
    employees_data = fetch_all_employees_details(year, month)
    drivers_data = fetch_all_drivers_details(year, month)

    employees = [Employee(**data) for data in employees_data]
    drivers = [Driver(**data) for data in drivers_data]

    _, days_in_month = calendar.monthrange(year, month)
    scheduler = ShiftScheduler(
        employees,
        drivers,
        days=range(days_in_month),
        work_types=['day_shift', 'night_shift'],
        public_holidays=holiday_set)

    result = scheduler.solve()
    return result
