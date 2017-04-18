class A(object):
    print('Setting class variables in A')
    aa_cls = 'class data, class A'

    def __init__(self):
        print('A: Initializing instance of', self.__class__.__name__)
        self.aa = 'instance data, class A'

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        print("A: Made instance of", self.__class__.__name__)
        return self

    def ameth(self):
        return "A method from class A"

class B(A):
    print('Setting class variables in B')
    bb_cls = 'class data, class B'

    def __init__(self):
        print('B: Initializing instance of', self.__class__.__name__)
        super().__init__()
        self.bb = 'instance data, class B'

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        print("B: Made instance of", self.__class__.__name__)
        return self

#print("Begin examination...")
#print("Data from classes:")
#print("A.aa_cls:", A.aa_cls)
#print("B.aa_cls:", B.aa_cls)

print("Instantiating A as a:")
a = A()
print("Instantiating B as b:")
b = B()

#print("Data from instance a:")
#print("a.aa_cls:", a.aa_cls)
#print("a.aa:", a.aa)
#print("call ameth directly from a:", a.ameth())
#print("Dict a:", a.__dict__)

#print("Data from instance b:")
#print("b.bb_cls:", b.bb_cls)
#print("b.bb:", b.bb)
#print("b.aa_cls:", b.aa_cls)
#print("call ameth from b:", b.ameth())
#print("b.aa:", b.aa)
#print("Dict b:", b.__dict__)

from pprint import pprint
print("A class info:", pprint(A.__class__.__dict__))
print("a instance info:", pprint(a.__class__))
print("B class info:", pprint(B.__class__))
print("b instance info:", pprint(b.__class__))
