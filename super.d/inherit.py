#!/usr/bin/python3

class A(object):
    def __init__(self):
        self.aa = 'instance of class A'

class B(A):
    def __init__(self):
        self.bb = 'instance of class B'

b = B()
print(b.aa)

