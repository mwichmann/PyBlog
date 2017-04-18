class A(object):

    def __init__(self, msg):
        print('A: Initializing instance of', self.__class__.__name__)
        self.message = msg

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        print("A: Made instance of", self.__class__.__name__)
        return self

class B(A):

    def __init__(self, msg, doinit=True):
        print('B: Initializing instance of', self.__class__.__name__)
        if doinit:
            super().__init__(msg)

    #def __new__(cls, msg, doinit=True):
    def __new__(cls, *args, **kwargs):
        #self = super().__new__(cls, None)
        self = super().__new__(cls, *args, **kwargs)
        print("B: Made instance of", self.__class__.__name__)
        return self

print("Instantiating an A:")
a = A("some message")
print(a.message)
print("Instantiating a B:")
b = B("some message")
print(b.message)
print("Instantiating a B without calling superclass __init__:")
c = B("some message", False)
print(c.message)
