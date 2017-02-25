
class A(object):
    def __init__(self):
        print('A: Initializing instance of', self.__class__.__name__)
        self.aa = 'instance of class A'

class B(A):
    def __init__(self):
        print('B: Initializing instance of', self.__class__.__name__)
        super().__init__()
        self.bb = 'instance of class B'

b = B()
print(b.aa)

print("Res order:", B.__mro__)

print("Dict:", b.__dict__)
print("dir:", dir(b))
