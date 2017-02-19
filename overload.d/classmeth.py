class Employee:
    num_of_emps = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        Employee.num_of_emps += 1

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)

    @classmethod
    def from_tuple(cls, first, last, pay):
        return cls(first, last, pay)

    def __str__(self):
        return "Name: {} {}, Pay: {}".format(self.first, self.last, self.pay)


emp_1 = Employee("John", "Public", 50000)
emp_2 = Employee.from_string("Test-Employee-60000")

print(emp_1)
print(emp_2)
print("Employees:", Employee.num_of_emps)
