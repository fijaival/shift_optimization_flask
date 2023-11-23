from .data_fetcher import fetch_all_employees, fetch_all_drivers, fetch_shift_requests_for_month, fetch_drivers_requests_for_month, fetch_qualifications, fetch_restrictions, fetch_all_dependencies, fetch_shifts_for_month, get_all_employees_details

from datetime import datetime

# Current year and month for demonstration
current_year = datetime.now().year
current_month = datetime.now().month


def totake():
    all_employees = fetch_all_employees()
    # print(all_employees)
    all_drivers = fetch_all_drivers()
    shift_requests_for_month = fetch_shift_requests_for_month(
        current_year, current_month)
    drivers_requests_for_month = fetch_drivers_requests_for_month(
        current_year, current_month)
    qualifications = fetch_qualifications()
    restrictions = fetch_restrictions()
    all_dependencies = fetch_all_dependencies()
    shifts_for_month = fetch_shifts_for_month(current_year, current_month-1)
    all = get_all_employees_details()

    return all
