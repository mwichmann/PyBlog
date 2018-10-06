class A(object):
    print('Setting class variables in A')
    clsdataA = 'class data, class A'

    def __init__(self):
        print('A: Initializing instance of', self.__class__.__name__)
        self.dataA = 'instance data, class A'

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        print("A: Made instance of", self.__class__.__name__)
        return self

    def methA(self):
        return "A method from class A"

class B(A):
    print('Setting class variables in B')
    clsdataB = 'class data, class B'

    def __init__(self):
        print('B: Initializing instance of', self.__class__.__name__)
        super().__init__()
        self.dataB = 'instance data, class B'

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        print("B: Made instance of", self.__class__.__name__)
        return self

#print("Begin examination...")
#print("Data from classes:")
#print("A.clsdataA:", A.clsdataA)
#print("B.clsdataA:", B.clsdataA)

print("Instantiating A as a:")
a = A()
print("Instantiating B as b:")
b = B()

#print("Data from instance a:")
#print("a.clsdataA:", a.clsdataA)
#print("a.dataA:", a.dataA)
#print("call methA directly from a:", a.methA())
#print("Dict a:", a.__dict__)

#print("Data from instance b:")
#print("b.clsdataB:", b.clsdataB)
#print("b.dataB:", b.dataB)
#print("b.clsdataA:", b.clsdataA)
#print("call methA from b:", b.methA())
#print("b.dataA:", b.dataA)
#print("Dict b:", b.__dict__)

from pprint import pprint
print("A class info:", pprint(A.__class__.__dict__))
print("a instance info:", pprint(a.__class__))
print("B class info:", pprint(B.__class__))
print("b instance info:", pprint(b.__class__))
