import pulp
import pandas as pd
import json

from .utils import get_consecutive_work_days, is_last_day_n


class ShiftScheduler:
    def __init__(self, employees, drivers, days, work_types, public_holidays):
        self.employees = employees
        self.drivers = drivers
        self.days = days
        self.work_types = work_types
        self.public_holidays = public_holidays
        self.prob = pulp.LpProblem("ShiftScheduling", pulp.LpMinimize)

    def create_variables(self):
        for employee in self.employees:
            employee.create_shift_variables(self.days, self.work_types)
            employee.create_penalty_variables(self.days)
        for driver in self.drivers:
            driver.create_shift_variables(self.days)
            driver.create_penalty_variables(self.days)

#######################
# 目的関数
#######################

    def set_objective(self):
        # 目的関数の設定
        self.prob += pulp.lpSum(
            employee.shift_vars[day, work_type]
            for employee in self.employees
            for day in self.days
            for work_type in self.work_types
        ) + pulp.lpSum(
            driver.shift_vars[day]
            for driver in self.drivers
            for day in self.days
        ) + pulp.lpSum(
            employee.penalty_vars[day]
            for employee in self.employees
            for day in self.days
        ) + pulp.lpSum(
            driver.penalty_vars[day]
            for driver in self.drivers
            for day in self.days
        )

#######################
# 制約関数
#######################

    def add_constraints(self):
        # 制約条件の追加
        self.caluculate_penalty()
        self.add_work_days_constraints()
        self.add_maximum_shifts_constraint()
        self.add_employee_count_constraints()
        self.add_no_seven_consecutive_work_days_constraint()
        self.add_all_off_if_qualified_constraint()
        self.add_daytime_consultant_constraint()
        self.add_nighttime_consultant_constraint()
        self.add_night_shift_followed_by_day_off_constraint()
        self.add_no_night_shift_if_not_qualified_constraint()
        self.add_no_day_shift_if_night_only_constraint()
        self.add_night_shift_limit_constraint()
        self.add_max_consecutive_work_constraint()
        self.add_driver_constraints()
#         self.add_dependency_constraints()
        self.including_last_month()

    # ペナルティの追加

    def caluculate_penalty(self):
        for employee in self.employees:
            for day in self.days:
                if day+1 in employee.shift_requests:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for work_type in self.work_types
                    ) <= employee.penalty_vars[day]

        for driver in self.drivers:
            for day in self.days:
                if day+1 in driver.driver_requests:
                    self.prob += driver.shift_vars[day] <= driver.penalty_vars[day]

    # 勤務日数
    def add_work_days_constraints(self):
        total_days = len(self.days)

        # 各従業員の勤務日数の制約
        for employee in self.employees:
            if "全部休み" not in employee.qualifications:
                paid_days = len(employee.paid)
                required_work_days = total_days - paid_days - self.public_holidays
                self.prob += pulp.lpSum(
                    employee.shift_vars[day, work_type] for day in self.days for work_type in self.work_types
                ) == required_work_days

        # 各ドライバーの勤務日数の制約
        for driver in self.drivers:
            off_requests = len(driver.driver_requests)
            required_work_days = total_days - off_requests
            self.prob += pulp.lpSum(
                driver.shift_vars[day] for day in self.days
            ) == required_work_days

    # 各従業員が1日に1つのシフトのみを担当する
    def add_maximum_shifts_constraint(self):
        for employee in self.employees:
            for day in self.days:
                self.prob += pulp.lpSum(
                    employee.shift_vars[day, work_type]
                    for work_type in self.work_types
                ) <= 1

    # 各日付の必要人員
    def add_employee_count_constraints(self):
        for day in self.days:
            # 日勤の従業員は1日10人以上
            self.prob += pulp.lpSum(
                employee.shift_vars[day, self.work_types[0]]
                for employee in self.employees
            ) >= 10
            # 夜勤の従業員数は1日3人以上
            self.prob += pulp.lpSum(
                employee.shift_vars[day, self.work_types[1]]
                for employee in self.employees
            ) >= 3

    # 7連勤の禁止
    def add_no_seven_consecutive_work_days_constraint(self):
        for employee in self.employees:
            for i in range(len(self.days) - 6):
                self.prob += pulp.lpSum(
                    employee.shift_vars[j, work_type]
                    for j in range(i, i + 7)
                    for work_type in self.work_types
                ) <= 6
        for driver in self.drivers:
            for i in range(len(self.days) - 6):
                self.prob += pulp.lpSum(
                    driver.shift_vars[j]
                    for j in range(i, i + 7)
                ) <= 6

    # 管理しない従業員
    def add_all_off_if_qualified_constraint(self):
        for employee in self.employees:
            if "全部休み" in employee.qualifications:
                for day in self.days:
                    for work_type in self.work_types:
                        self.prob += employee.shift_vars[day, work_type] == 0

    # 日勤有資格者３人以上
    def add_daytime_consultant_constraint(self):
        for day in self.days:
            self.prob += pulp.lpSum(
                employee.shift_vars[day, 'day_shift']
                for employee in self.employees if "日勤相談員" in employee.qualifications
            ) >= 3

    # 夜勤有資格者1人以上
    def add_nighttime_consultant_constraint(self):
        for day in self.days:
            self.prob += pulp.lpSum(
                employee.shift_vars[day, 'night_shift']
                for employee in self.employees if "夜勤相談員" in employee.qualifications
            ) >= 1

    # 夜勤の翌日は休み
    def add_night_shift_followed_by_day_off_constraint(self):
        for employee in self.employees:
            if "夜勤固定" not in employee.qualifications:
                for day in range(len(self.days) - 1):
                    self.prob += (
                        employee.shift_vars[self.days[day], 'night_shift'] +
                        pulp.lpSum(
                            employee.shift_vars[self.days[day + 1], work_type] for work_type in self.work_types)
                    ) <= 1

    # 夜勤不可が夜勤に入らない
    def add_no_night_shift_if_not_qualified_constraint(self):
        for employee in self.employees:
            if "夜勤不可" in employee.qualifications:
                for day in self.days:
                    self.prob += employee.shift_vars[day, 'night_shift'] == 0

    # 夜勤組は日勤には入らない
    def add_no_day_shift_if_night_only_constraint(self):
        for employee in self.employees:
            if "夜勤固定" in employee.qualifications:
                for day in self.days:
                    self.prob += employee.shift_vars[day, 'day_shift'] == 0

    # 夜勤回数制限ある人
    def add_night_shift_limit_constraint(self):
        for employee in self.employees:
            night_shift_limit = next(
                (r['value'] for r in employee.restrictions if r['name'] == '夜勤の回数制限'), None)
            if night_shift_limit is not None:
                self.prob += pulp.lpSum(
                    employee.shift_vars[day, 'night_shift'] for day in self.days
                ) <= night_shift_limit

    # 連続勤務条件がある人
    def add_max_consecutive_work_constraint(self):
        for employee in self.employees:
            max_consecutive = next(
                (r['value'] for r in employee.restrictions if r['name'] == '連続勤務'), None)
            if max_consecutive is not None:
                for start_day in range(len(self.days) - max_consecutive):
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for day in self.days[start_day:start_day + max_consecutive + 1] for work_type in self.work_types
                    ) <= max_consecutive

    # 運転手６人以上
    def add_driver_constraints(self):
        for day in self.days:
            driving_employees_count = pulp.lpSum(
                employee.shift_vars[day, 'day_shift']
                for employee in self.employees if "運転可能" in employee.qualifications
            )
            drivers_count = pulp.lpSum(
                driver.shift_vars[day] for driver in self.drivers
            )
            self.prob += driving_employees_count + drivers_count >= 6

    # 依存関係
#     def add_dependency_constraints(self):
#         for employee in self.employees:
#             if employee.dependencies:  # 依存関係がある場合のみ処理
#                 for day in self.days:
# #                     for work_type in self.work_types:
#                         # 依存元の従業員がシフトに入る場合、依存先の従業員もシフトに入る制約を追加
#                         for dep_id in employee.dependencies:
#                             dependent_employee = next((e for e in self.employees if e.id == dep_id), None)
#                             if dependent_employee:
#                                 self.prob += (
#                                     dependent_employee.shift_vars[day, "night_shift"] -
#                                     employee.shift_vars[day, "night_shift"]
#                                 ) >= 0

    # 先月分考慮
    def including_last_month(self):
        for employee in self.employees:
            continuous_work = get_consecutive_work_days(
                employee.last_month_shifts)
            is_last_night = is_last_day_n(employee.last_month_shifts)
            if continuous_work == 0:
                continue

            # 7連勤の禁止
            self.prob += pulp.lpSum(
                employee.shift_vars[day, work_type] for work_type in self.work_types for day in range(7 - continuous_work)
            ) <= 6 - continuous_work

            # 夜勤の次の日休み
            if is_last_night == 1 and "夜勤固定" not in employee.qualifications:
                self.prob += pulp.lpSum(
                    employee.shift_vars[self.days[0], work_type] for work_type in self.work_types
                ) == 0

            # 連続勤務条件
            max_consecutive = next(
                (r['value'] for r in employee.restrictions if r['name'] == '連続勤務'), None)
            if max_consecutive is not None:
                if max_consecutive < continuous_work:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[self.days[0], work_type] for work_type in self.work_types
                    ) == 0
                else:
                    self.prob += pulp.lpSum(
                        employee.shift_vars[day, work_type] for work_type in self.work_types for day in range(max_consecutive - continuous_work + 1)
                    ) <= max_consecutive - continuous_work


#######################
# 実行
#######################

    def solve(self):
        self.create_variables()
        self.set_objective()
        self.add_constraints()
        self.prob.solve()
        # 問題を解く
        solution_status = pulp.LpStatus[self.prob.status]

        if solution_status == 'Optimal':
            employees_schedule = self.display_employees_schedule()
            drivers_schedule = self.display_drivers_schedule()
            unwanted_employees_shifts, unwanted_drivers_shifts = self.display_unwanted_shifts()

            # 結果を辞書にまとめる
            result = {
                "employees_schedule": json.loads(employees_schedule),
                "drivers_schedule": json.loads(drivers_schedule),
                "unwanted_employees_shifts": unwanted_employees_shifts,
                "unwanted_drivers_shifts": unwanted_drivers_shifts
            }

            # 辞書をJSONに変換
            return json.dumps(result, ensure_ascii=False)
        else:
            return json.dumps({"message": "No optimal solution found."}, ensure_ascii=False)


#######################
# 結果の表示
#######################

    def display_employees_schedule(self):
        day_labels = [f"{day+1}日" for day in self.days]

        # 従業員
        schedule_df = pd.DataFrame(
            index=[e.id for e in self.employees], columns=day_labels)
        for employee in self.employees:
            for day in self.days:
                shift_assigned = False
                for work_type in self.work_types:
                    if pulp.value(employee.shift_vars[day, work_type]) == 1:
                        if work_type == "night_shift":
                            schedule_df.at[employee.id, f"{day+1}日"] = "N"
                        else:
                            schedule_df.at[employee.id, f"{day+1}日"] = "日勤"
                        shift_assigned = True
                        break
                if not shift_assigned:
                    if day+1 in employee.paid:
                        schedule_df.at[employee.id, f"{day+1}日"] = '有'
                    else:
                        schedule_df.at[employee.id, f"{day+1}日"] = '公'
            schedule_df = schedule_df.rename(
                index={employee.id: employee.name})

        employees_schedule = schedule_df.to_json(force_ascii=False)
        return employees_schedule

    def display_drivers_schedule(self):
        day_labels = [f"{day+1}日" for day in self.days]

        # ドライバー
        driver_schedule_df = pd.DataFrame(
            index=[d.id for d in self.drivers], columns=day_labels)
        for driver in self.drivers:
            for day in self.days:
                if pulp.value(driver.shift_vars[day]) == 1:
                    driver_schedule_df.at[driver.id, f"{day+1}日"] = "〇"
                elif day+1 in driver.paid:
                    driver_schedule_df.at[driver.id, f"{day+1}日"] = "有"
                else:
                    driver_schedule_df.at[driver.id, f"{day+1}日"] = "公"
            driver_schedule_df = driver_schedule_df.rename(
                index={driver.id: driver.name})

        drivers_schedule = driver_schedule_df.to_json(force_ascii=False)
        return drivers_schedule

    def display_unwanted_shifts(self):
        unwanted_employees_shifts = {}
        for employee in self.employees:
            unwanted = []
            for day in self.days:
                if pulp.value(employee.penalty_vars[day]) == 1:
                    unwanted.append(day+1)
            if unwanted:
                unwanted_employees_shifts[employee.id] = unwanted

        unwanted_drivers_shifts = {}
        for driver in self.drivers:
            unwanted = []
            for day in self.days:
                if pulp.value(driver.penalty_vars[day]) == 1:
                    unwanted.append(day+1)
            if unwanted:
                unwanted_drivers_shifts[driver.id] = unwanted
        return unwanted_employees_shifts, unwanted_drivers_shifts
