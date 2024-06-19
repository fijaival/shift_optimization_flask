import pulp


class Employee:
    def __init__(self, employee_id, name, qualifications, day_off_requests, full_time=False):
        self.employee_id = employee_id
        self.name = name
        self.qualifications = qualifications
        self.day_off_requests = day_off_requests
        self.full_time = full_time
        self.shift_vars = {}
        self.penalty_vars = {}
        self.assigned_vars = {}
        self.paid_vars = {}

    def create_shift_variables(self, days, work_types):
        for day in days:
            for work_type in work_types:
                var_name = f"x_{self.employee_id}_{day}_{work_type}"
                self.shift_vars[(day, work_type)] = pulp.LpVariable(var_name, 0, 1, cat='Binary')

    def create_penalty_variables(self, weeks_in_month):
        for week in range(weeks_in_month):
            var_name = f"penalty_{self.employee_id}_week_{week}"
            self.penalty_vars[week] = pulp.LpVariable(var_name, 0, 1, cat='Binary')

    def create_assigned_vars(self, days):
        for day in days:
            var_name = f"assigned_{self.employee_id}_{day}"
            self.assigned_vars[day] = pulp.LpVariable(var_name, 0, 1, cat='Binary')

    def create_paid_vars(self, days):
        for day in days:
            var_name = f"paid_{self.employee_id}_{day}"
            self.paid_vars[day] = pulp.LpVariable(var_name, 0, 1, cat='Binary')
