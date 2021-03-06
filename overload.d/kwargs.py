class Employee:
    num_of_emps = 0

    def __init__(self, **kwargs):
        if "emp_str" in kwargs:
            first, last, pay = kwargs["emp_str"].split('-')
        elif "first" in kwargs and "last" in kwargs and "pay" in kwargs:
            first = kwargs["first"]
            last = kwargs["last"]
            pay = kwargs["pay"]
        else:
            print("invalid initializer")
            return

        self.first = first
        self.last = last
        self.pay = pay
        Employee.num_of_emps += 1

    def __str__(self):
        return "Name: {} {}, Pay: {}".format(self.first, self.last, self.pay)


emp_1 = Employee(first="John", last="Public", pay=50000)
emp_2 = Employee(emp_str="Test-Employee-60000")

print(emp_1)
print(emp_2)
print("Employees:", Employee.num_of_emps)