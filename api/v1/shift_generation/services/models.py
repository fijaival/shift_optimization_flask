import pulp


class Employee:
    def __init__(self, dependencies, id, last_month_shifts, name, paid, qualifications, restrictions, shift_requests):
        self.id = id
        self.name = name
        self.qualifications = qualifications
        self.restrictions = restrictions
        self.shift_requests = shift_requests
        self.dependencies = dependencies
        self.paid = paid
        self.last_month_shifts = last_month_shifts
        self.shift_vars = {}
        self.penalty_vars = {}

    def create_shift_variables(self, days, work_types):
        for day in days:
            for work_type in work_types:
                var_name = f"x({self.id},{day},{work_type})"
                self.shift_vars[(day, work_type)] = pulp.LpVariable(
                    var_name, cat="Binary")

    def create_penalty_variables(self, days):
        for day in days:
            var_name = f"penalty({self.id},{day+1})"
            self.penalty_vars[day] = pulp.LpVariable(
                var_name, 0, 1, cat="Binary")


class Driver:
    def __init__(self, driver_requests, id, name, paid):
        self.id = id
        self.name = name
        self.driver_requests = driver_requests
        self.paid = paid
        self.shift_vars = {}
        self.penalty_vars = {}

    def create_shift_variables(self, days):
        for day in days:
            var_name = f"x({self.id},{day})"
            self.shift_vars[(day)] = pulp.LpVariable(var_name, cat="Binary")

    def create_penalty_variables(self, days):
        for day in days:
            var_name = f"driver_penalty({self.id},{day+1})"
            self.penalty_vars[day] = pulp.LpVariable(
                var_name, 0, 1, cat="Binary")
