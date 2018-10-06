class A(object):
    def __init__(self):
        self.dataA = 'instance of class A'

class B(A):
    def __init__(self):
        self.dataB = 'instance of class B'

b = B()
print("b.dataA:", b.dataA)
