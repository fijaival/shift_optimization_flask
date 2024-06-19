from .shiftScheduler import ShiftScheduler
from datetime import datetime
import math

import calendar
import pulp
import re


class HanazonoFacilityOptimizeService(ShiftScheduler):
    def __init__(self, employees, day_off_requests, year, month):
        super().__init__(year, month)
        self.employees = employees
        self.day_off_requests = day_off_requests
        self.year = year
        self.month = month
        self.prob = pulp.LpProblem("ShiftScheduling", pulp.LpMinimize)
        self.work_types = ['day1', 'day2', 'day3', 'evening1', 'evening2', 'evening3']
        self.days = range(1, calendar.monthrange(year, month)[1] + 1)
        self.absolute_min_workers_per_day = 5
        self.sacrificed_work = "evening1"
        self.penalty_vars = {}

    def create_variables(self):
        _, _, weeks_in_month = self.calculate_days()
        for employee in self.employees:
            employee.create_shift_variables(self.days, self.work_types)
            employee.create_penalty_variables(weeks_in_month)
            employee.create_assigned_vars(self.days)
            employee.create_paid_vars(self.days)

        for day in self.days:
            var_name = f"penalty_d_{day}"
            self.penalty_vars[day] = pulp.LpVariable(var_name, 0, 1, cat="Binary")

    def set_objective(self):
        penalty_for_not_assigning_sacrificed_work = 100
        penalty_for_over_work = 200
        self.prob += pulp.lpSum(
            employee.shift_vars[day, work_type]
            for employee in self.employees
            for day in self.days
            for work_type in self.work_types
        ) + pulp.lpSum(
            penalty_for_over_work * employee.penalty_vars[week]
            for employee in self.employees
            for week in range(len(employee.penalty_vars))
        ) + pulp.lpSum(
            penalty_for_not_assigning_sacrificed_work * self.penalty_vars[day]
            for day in self.days
        )

    def calculate_days(self):
        first_day_of_month = datetime(self.year, self.month, 1)
        first_sunday = 1 if first_day_of_month.weekday() == 6 else 7 - first_day_of_month.weekday()
        first_sunday = first_sunday - 1
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        weeks_in_month = math.floor((days_in_month - first_sunday + 1) / 7)
        return first_sunday, days_in_month, weeks_in_month

    def add_constraints(self):
        self.add_constraint_for_unassigned_work_penalty()
        self.add_constraint_for_day_off_requests()
        self.add_constraint_for_one_worker_per_day()
        self.add_constraint_for_minimum_workers_per_day()
        self.add_constraint_for_minimum_workers_per_worktype()
        self.add_constraint_for_no_work_on_paid_off()
        self.add_constraint_for_allowed_work_types()
        self.add_constraint_for_weekly_working_days()
        self.add_constraint_for_daily_assignment()
        self.add_constraint_for_no_consecutive_work_days()
        self.add_constraint_for_all_employees_third_thursday_attendance()
        self.add_constraint_for_individual_employee()

    def add_constraint_for_unassigned_work_penalty(self):
        for day in self.days:
            self.prob += (
                pulp.lpSum(employee.shift_vars[day, self.sacrificed_work]
                           for employee in self.employees) + self.penalty_vars[day] >= 1,
                f"Penalty_if_no_{self.sacrificed_work}_on_day_{day}"
            )

    def add_constraint_for_day_off_requests(self):
        for employee in self.employees:
            for day in employee.day_off_requests:
                self.prob += employee.assigned_vars[day] <= 0

    def add_constraint_for_one_worker_per_day(self):
        for day in self.days:
            for employee in self.employees:
                if not employee.full_time:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for work_type in self.work_types
                    ) <= 1, f"{employee}_{day}_can_one_work"
                else:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for work_type in self.work_types
                    ) <= 2, f"{employee}_{day}_can_two_work"
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, self.work_types[i]] for i in range(3)
                    ) <= 1, f"{employee}_{day}_can_one_daywork"
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, self.work_types[i]] for i in range(3, 6)
                    ) <= 1, f"{employee}_{day}_can_one_eveningwork"

    def add_constraint_for_minimum_workers_per_day(self):
        for day in self.days:
            self.prob += pulp.lpSum(
                employee.shift_vars[day, work_type] for employee in self.employees for work_type in self.work_types
            ) >= self.absolute_min_workers_per_day, f"Min_workers_day_{day}"

    def add_constraint_for_minimum_workers_per_worktype(self):
        for day in self.days:
            for work_type in self.work_types:
                if work_type != self.sacrificed_work:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for employee in self.employees
                    ) >= 1

    def add_constraint_for_no_work_on_paid_off(self):
        for employee in self.employees:
            self.prob += pulp.lpSum(
                employee.paid_vars[day] for day in self.days
            ) == employee.paid_off
            for day in self.days:
                self.prob += employee.assigned_vars[day] + employee.paid_vars[day] <= 1

    def add_constraint_for_allowed_work_types(self):
        for employee in self.employees:
            for day in self.days:
                for work_type in self.work_types:
                    if work_type not in employee.qualifications:
                        self.prob += employee.shift_vars[(day, work_type)] == 0

    def add_constraint_for_weekly_working_days(self):
        first_sunday, days_in_month, weeks_in_month = self.calculate_days()
        for employee in self.employees:
            for week in range(weeks_in_month):
                start_day = first_sunday + week * 7
                end_day = start_day + 7
                self.prob += pulp.lpSum(employee.shift_vars[(day, work_type)]
                                        for day in range(start_day, end_day)
                                        for work_type in self.work_types) <= employee.weekly_days

    def add_constraint_for_daily_assignment(self):
        for employee in self.employees:
            for day in self.days:
                self.prob += employee.assigned_vars[day] >= pulp.lpSum(employee.shift_vars[(day, work_type)]
                                                                       for work_type in self.work_types) * (1 / len(self.work_types))

    def add_constraint_for_no_consecutive_work_days(self):
        for employee in self.employees:
            for start_day in range(len(self.days) - 4):
                consecutive_days_work = pulp.lpSum(
                    employee.assigned_vars[day] for day in range(start_day, start_day + 5))
                paid_off = pulp.lpSum(employee.paid_vars[day] for day in range(start_day, start_day + 5))
                self.prob += consecutive_days_work + \
                    paid_off <= 4, f"no_consecutive_5_days_work_{employee.employee_id}_{start_day}"

    def add_constraint_for_all_employees_third_thursday_attendance(self):
        first_sunday, _, _ = self.calculate_days()
        if first_sunday >= 3:
            the_third_Thursday = first_sunday + 11
        else:
            the_third_Thursday = first_sunday + 18

        for i in range(6):
            self.prob += pulp.lpSum(employee.shift_vars[(the_third_Thursday, self.work_types[i])]
                                    for employee in self.employees) >= 1, f"third_thursday_{self.work_types[i]}"

    def add_constraint_for_individual_employee(self):
        for employee in self.employees:
            if employee.employee_id == 1:
                for start_day in range(len(self.days) - 2):
                    consecutive_days_work = pulp.lpSum(
                        employee.assigned_vars[day] for day in range(start_day, start_day + 3))
                    paid_off = pulp.lpSum(employee.paid_vars[day] for day in range(start_day, start_day + 3))
                    self.prob += consecutive_days_work + \
                        paid_off <= 2, f"no_consecutive_3_days_work_{employee.employee_id}_{start_day}"
                for start_day in range(len(self.days) - 1):
                    is_assigned_today_evning_work = pulp.lpSum(employee.shift_vars[(start_day, self.work_types[i])]
                                                               for i in range(3, 6))
                    is_assigned_tommorow_day_work = pulp.lpSum(employee.shift_vars[(start_day + 1, self.work_types[i])]
                                                               for i in range(3))
                    self.prob += is_assigned_today_evning_work + is_assigned_tommorow_day_work <= 1

            if employee.employee_id == 5:
                holidays = []
                first_sunday, _, _ = self.calculate_days()
                for day in range(len(self.days)):
                    if day % 7 == (first_sunday + 5) % 7 or day % 7 == (first_sunday + 6) % 7:
                        holidays.append(day)
                self.prob += pulp.lpSum(employee.assigned_vars[holiday]
                                        for holiday in holidays) <= len(holidays) - 2, f"week_end_day_off_for_{employee.employee_id}"

                for day in self.days:
                    self.prob += pulp.lpSum(employee.shift_vars[(day, self.work_types[4])]) <= pulp.lpSum(emp.shift_vars[(day, self.work_types[3])]
                                                                                                          for emp in self.employees)

    def create_employees_schedule(self):
        num_days = calendar.monthrange(self.year, self.month)[1]
        schedule = {day: [] for day in range(1, num_days + 1)}

        for employee in self.employees:
            for day in self.days:
                assigned_works = [work_type for work_type in self.work_types if pulp.value(
                    employee.shift_vars[day, work_type]) == 1]
                if pulp.value(employee.paid_vars[day]) == 1:
                    schedule[day].append(f"{employee.name} - 有休")
                elif day in employee.day_off_requests:
                    continue
                elif not assigned_works:
                    schedule[day].append(f"{employee.name} - 休み")
                else:
                    for work in assigned_works:
                        schedule[day].append(f"{employee.name} - {self.replace_text(work)}")

        return schedule

    def replace_text(self, text):
        match = re.match(r'day(\d+)', text)
        if match:
            return f'昼{match.group(1)}'
        match = re.match(r'evening(\d+)', text)
        if match:
            return f'夕{match.group(1)}'
        return text

    def solve(self):
        self.create_variables()
        self.set_objective()
        self.add_constraints()
        self.prob.solve()
        solution_status = pulp.LpStatus[self.prob.status]

        if solution_status == 'Optimal':
            schedule = self.create_employees_schedule()
            return schedule
        else:
            return None
