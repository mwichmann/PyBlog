
Python Test Driven Development Basics with PyTest
#################################################

Introduction
============

Not long ago I was chatting with someone about some code he was working
on that did something some might consider "obscure", and how to be sure
it worked correctly.  You can of course put in print statements to trace
what is going on, then remove them later, but this also sounds like
a case for writing a test that confirms the behavior, then coding up
the function, making adjustments until the test passes.  This roughly,
is what is called test-driven development (TDD).

When we chatted about how to do that, the person said they had trouble
working with the Python unittest module, and I pointed out I don't
much care for it either.  One reason is because it forces you to use
classes even when it may not feel all that natural to write a class for
a particular problem. I wrote up some notes for him on using PyTest,
and then decided to modify those for somewhat wider sharing.

So here's a vaguely practical example of applying the pattern that
led to our discussion, that is how to effectively run a test function
several different ways, rather than writing up a function for each
permutation of your test.

First, and immediately violating the principles of TDD which say to
write the test first, let's write the function to test.  Our candidate
function tries to return the reverse of its argument, to keep it simple,
we will assume the argument is something that can be iterated over,
so we can use fancy list slicing (thus we can't reverse a dictionary -
but that has no meaning anyway since a dictionary has no order).  To show
it's working there is also code to try it out if it is called as a program
(as opposed to a module). This is the way people used to write tests for
a Python module, before test harnesses became widely used: just code up
a few checks and stuff them into the "main" part::

    def slicerev(collection):
        return collection[::-1]

    if __name__ == "__main__":
        print slicerev([1,2,3,4])
        print slicerev((1,2,3,4))
        print slicerev('abcd')

If we run that, we see that all of list, tuple and string did indeed
get reversed as we expected::

    [4, 3, 2, 1]
    (4, 3, 2, 1)
    dcba


Using PyTest
============

Let's take this basic test code and turn it into a separate test using
PyTest.  Unit tests for a particular function are often named (this is
convention) test\_{funcname}.py. If it's named this way lets pytest discover
it automatically - runing py.test without arguments lets it hunt for
files that begin with 'test\_' or end with '_test'.  It's not mandatory to use this naming,
you can give the name of the test file as an argument, or use other
methods to describe exactly where the tests should be picked up from.

The code can be really simple since this is a contrived example - we're
not really systematically "unit testing", we're spot checking.  All we
have to do is import the function we are going to test (even this is
not needed if the test is in the same file as the code being tested,
as opposed to a separate file), and then write out our three test cases,
which do nothing but call the function with a known argument, then
compare the return with what we expect the result to be. ::

    from reverser import slicerev

    def test_slicerev_list():
        output = slicerev([1,2,3,4])
        assert output == [4,3,2,1]

    def test_slicerev_tuple():
        output = slicerev((1,2,3,4))
        assert output == (4,3,2,1)

    def test_slicerev_string():
        output = slicerev('abcd')
        assert output == 'edcba'

That's really all there is to it.

To make things a little more interesting, I have introduced an error in
the test itself: the function checking the reversed string claims it
expects 'edcba' instead of 'dcba'. This is done to show what it looks
like when PyTest reports a failure.

Let's run it::

    $ py.test test_slicerev.py
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.13, pytest-2.9.2, py-1.4.33, pluggy-0.3.1
    rootdir: /home/mats/PyBlog/pytester.d, inifile: 
    collected 3 items

    test_slicerev.py ..F

    =================================== FAILURES ===================================
    _____________________________ test_slicerev_string _____________________________

        def test_slicerev_string():
            output = slicerev('abcd')
    >       assert output == 'edcba'
    E       assert 'dcba' == 'edcba'
    E         - dcba
    E         + edcba
    E         ? +

    test_slicerev.py:13: AssertionError
    ====================== 1 failed, 2 passed in 0.01 seconds ======================

A run with that problem fixed is considerably quieter::

    $ py.test test_slicerev.py
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.13, pytest-2.9.2, py-1.4.33, pluggy-0.3.1
    rootdir: /home/mats/PyBlog/pytester.d, inifile: 
    collected 3 items 

    test_slicerev.py ...

    =========================== 3 passed in 0.00 seconds ==========================


PyTest Fixtures
===============

If you think about this for a bit, you notice that the same code is
run three times, only the data in the three test functions differs.
As mentioned above, this is a very common situation in testing, where
you want to try different cases to see how a unit behaves - test the
boundary conditions, test invalid data or data types, etc.

PyTest provides a mechanism called a "fixture" - a fixed baseline that
can be executed repeatedly, which helps with this situation.

In the first iteration of our tests, we did not need to import "pytest"
for it to work when the test is run by PyTest - PyTest wraps the code and
the code itself never uses anything from PyTest. However, in our second
iteration, we do want something from PyTest namespace - the definition
of the decorator we need to turn something into a PyTest fixture, so
the import is needed.

Since what we're factoring here is supplying different sets of data, the
fixture function `slicedata` itself is extremely simple: all it does is
return the data.  The test function has the same two functional statements
that each of the test functions had before - call the function under test,
then use an assertion to check the result was as expected.  In addition
to that, the test takes the fixture function as an argument, which would not
make much sense by itself, but once it is turned into a fixture it does.

We use a decorator to turn 'slicedata' into a fixture - remember Python
decorators are a piece of special syntax that helps alter the behavor
of a function.  The PyTest fixture decorator can take a "params" parameter,
which should be something that can be iterated over, the fixture function
can then receive the data one at a time.  In this case we are going
to pass a list of tuples, the first element of each tuple being the
data we are going to apply to the test, the second element being the
expected value.

We now know the other change we need to make to the test function:
the "fixture object" returned by the fixture will be a tuple, so
we should unpack the tuple into the pieces we want.

The new code looks like this::

    import pytest
    from reverser import slicerev

    @pytest.fixture(params=[
        ([1,2,3,4], [4,3,2,1]),
        ((1,2,3,4), (4,3,2,1)),
        ('abcd',    'dcba')
        ])
    def slicedata(request):
        return request.param

    def test_slicerev(slicedata):
        input, expected = slicedata
        output = slicerev(input)
        assert output == expected

Run these tests and we'll see the results are the same as before::

    $ py.test test_slicerev_fix.py
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.13, pytest-2.9.2, py-1.4.33, pluggy-0.3.1
    rootdir: /home/mats/PyBlog/pytester.d, inifile: 
    collected 3 items 

    test_slicerev_fix.py ...

    =========================== 3 passed in 0.00 seconds ===========================
