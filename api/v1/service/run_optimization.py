from api.error import InvalidAPIUsage
from .scheduler import facility_class_map
from .day_off_requests import get_all_requests_services
from .employees import get_all_employees_service


def run_optimization(facility_id, year, month):
    employees_data = get_all_employees_service(facility_id)
    day_off_requests = get_all_requests_services(facility_id, year, month)
    scheduler_class = facility_class_map.get(facility_id)
    if not scheduler_class:
        return None

    # scheduler = scheduler_class(employees_data, day_off_requests, int(year), int(month))
    # result = scheduler.solve()
    # if result is None:
    #     raise InvalidAPIUsage("No optimal solution found.", 500)
    # return result
    return demo_data


demo_data = [
    {"employee_id": 1, "date": "2024-06-01", "type_of_work": "day1"},
    {"employee_id": 2, "date": "2024-06-02", "type_of_work": "day2"},
    {"employee_id": 3, "date": "2024-06-03", "type_of_work": "day3"},
    {"employee_id": 4, "date": "2024-06-04", "type_of_work": "evening1"},
    {"employee_id": 5, "date": "2024-06-05", "type_of_work": "evening2"},
    {"employee_id": 6, "date": "2024-06-06", "type_of_work": "evening3"},
    {"employee_id": 7, "date": "2024-06-07", "type_of_work": "day1"},
    {"employee_id": 8, "date": "2024-06-08", "type_of_work": "day2"},
    {"employee_id": 9, "date": "2024-06-09", "type_of_work": "day3"},
    {"employee_id": 10, "date": "2024-06-10", "type_of_work": "evening1"},
    {"employee_id": 1, "date": "2024-06-11", "type_of_work": "evening2"},
    {"employee_id": 2, "date": "2024-06-12", "type_of_work": "evening3"},
    {"employee_id": 3, "date": "2024-06-13", "type_of_work": "day1"},
    {"employee_id": 4, "date": "2024-06-14", "type_of_work": "day2"},
    {"employee_id": 5, "date": "2024-06-15", "type_of_work": "day3"},
    {"employee_id": 6, "date": "2024-06-16", "type_of_work": "evening1"},
    {"employee_id": 7, "date": "2024-06-17", "type_of_work": "evening2"},
    {"employee_id": 8, "date": "2024-06-18", "type_of_work": "evening3"},
    {"employee_id": 9, "date": "2024-06-19", "type_of_work": "day1"},
    {"employee_id": 10, "date": "2024-06-20", "type_of_work": "day2"},
    {"employee_id": 1, "date": "2024-06-21", "type_of_work": "day3"},
    {"employee_id": 2, "date": "2024-06-22", "type_of_work": "evening1"},
    {"employee_id": 3, "date": "2024-06-23", "type_of_work": "evening2"},
    {"employee_id": 4, "date": "2024-06-24", "type_of_work": "evening3"},
    {"employee_id": 5, "date": "2024-06-25", "type_of_work": "day1"},
    {"employee_id": 6, "date": "2024-06-26", "type_of_work": "day2"},
    {"employee_id": 7, "date": "2024-06-27", "type_of_work": "day3"},
    {"employee_id": 8, "date": "2024-06-28", "type_of_work": "evening1"},
    {"employee_id": 9, "date": "2024-06-29", "type_of_work": "evening2"},
    {"employee_id": 10, "date": "2024-06-30", "type_of_work": "evening3"}
]
