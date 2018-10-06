class A(object):
    print('Setting class variables in A')
    clsdataA = 'class A'

    def __init__(self):
        print('Initializing instance of', self.__class__.__name__)
        self.dataA = 'instance of class A'

    def methA(self):
        return "A method from class A"

class B(A):
    print('Setting class variables in B')
    clsdataB = 'class B'

    def __init__(self):
        print('Initializing instance of', self.__class__.__name__)
        self.dataB = 'instance of class B'

print("Begin examination...")
print("Data from classes:")
print("A.clsdataA:", A.clsdataA)
print("B.clsdataA:", B.clsdataA)

print("Instantiating A as a:")
a = A()
print("Data from instance a:")
print("a.clsdataA:", a.clsdataA)
print("a.dataA:", a.dataA)
print("call methA directly from a:", a.methA())

print("Instantiating B as b:")
b = B()
print("Data from instance b:")
print("b.clsdataB:", b.clsdataB)
print("b.dataB:", b.dataB)
print("b.clsdataA:", b.clsdataA)
print("call methA from b:", b.methA())
print("b.dataA:", b.dataA)
