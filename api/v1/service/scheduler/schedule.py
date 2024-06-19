class Schedule:
    def __init__(self):
        self.shifts = []
        self.assignments = {}

    def add_shift(self, shift):
        self.shifts.append(shift)

    def assign_employee_to_shift(self, employee, shift):
        if shift.shift_id not in self.assignments:
            self.assignments[shift.shift_id] = []
        self.assignments[shift.shift_id].append(employee)
