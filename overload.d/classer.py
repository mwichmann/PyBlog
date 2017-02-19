class Foo:
    def a(self):
        print "Hello"

    def a(self, x):
        print "Hi, argument was", x

b = Foo()
b.a()
b.a("hello")

