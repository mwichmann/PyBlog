################################################
The Python "with" statement and Context Managers
################################################

Introduction
============

The Python "with" statement helps when you want to refactor code that
follows a particular pattern, roughly along these lines::

    # set things up
    try:
        # do something
    finally:
        # tear things down

When do you need this sort of code?  When there's some resource you
need access to, but don't have to (and should not) hold on to forever.
The two most common cases, I believe, are file descriptors (open files)
and thread synchronization (using mutex locks).  A bit of googling would
turn up lots of articles and forum posts that look like "Python whatsit
leaks file descriptors", "Python subprocess runs out of file descriptors",
etc. Managing file descriptor usage can be quite tricky if the opened
file descriptors are used all over the place; if that situation exists
perhaps some other refactoring is also in order.  Locks are a little
simpler, they exist to manipulate something which could have concurrent
access problems, and programmers know that section should be as short
as possible, so the usage doesn't tend to scatter all over the place,
but it's still easy to get into trouble, as an example below will show.

Here's a simple snippet using a try/finally block to manage file opens,
this sort of thing, a decade or more ago, was a common idiom for working
with an external file::

    outfile = open("foo.txt", "w")
    try:
        outfile.write('foo')
    finally:
        outfile.close()

To be pedantic, the file open could fail, for example if the file could
already exists and not have write permission, so possibly the open should
also be wrapped in a try block.

Anyway, if you don't make sure a file close happens, and there are lots
of files to open, you will eventually run out of the system resource
that is file descriptors.

Here's a snippet using locks::

    from threading import Lock

    lock = Lock()
    lock.acquire()
    try:
        my_list.append(item)
    finally:
        lock.release()

Handling locks carefully is really important.  Here's a different (very
artificial, and probably not too realistic) snippet that shows how to
get into trouble::

    def some_critical_section(my_list, item):
        lock.acquire()
        my_list.append(item)
        return 'some kind of error here'
        lock.release()

In other words, "something happens" somewhere between the acquire and
release, and we drop out of the function without the lock ever being
released.  Future calls to this function will block trying to acquire
the lock that they'll never get. You have to write carefully not to
get into such deadlock situations, once code complexity rises. Did you
anticipate the possible error exits, and release the lock in all of them?

The "with" statment
===================

Both of the file open and thread lock examples follow the
pattern shown at the beginning.  In Python 2.5 (as described by
`[PEP 343] <https://www.python.org/dev/peps/pep-0343>`_), a bit of new syntax
was introduced to help write things using this pattern more concisely,
and thus hopefully more clearly. The new keyword "with" was introduced,
and it can take a companion "as" clause.  Using "with" sets up a context
that Python keeps track of, wrapping it in appropriate begin/end logic.

Using it is pretty simple::

    from threading import Lock

    lock = Lock()
    with lock:
        my_list.append(item)

If you need a handle to the resource being acquired, which is usually
the case, you can save that by adding an "as" clause, like this::

    with open("foo.txt", "w") as outfile:
         outfile.write('foo')

The block following the "with" statement is the context, and Python
takes care of wrapping beginning and ending steps around that context.
The above are the new idioms for dealing with these kinds of resources,
and probably most people who have learned Python from 2.6 on know these
(I said earlier "with" was introduced in Python 2.5, but there it was
available only as a "future" feature, 2.6 is where it really became
mainstream) - but perhaps don't understand why. The why is a cleaner
syntax and cleaner concept of what the "context" section is.

Context Managers
================

Notice in the "with" versions of the examples there appear to be
details missing: in the lock example, lock.acquire() and lock.release()
are not mentioned; in the file open example the outfile.close()
is not present - which leads to the question "how does Python
know what to do here?".  It turns out that using the "with"
statement requires help from something called a Context Manager,
which is a class which follows the context management protocol.  The
`Python Documentation 
<https://docs.python.org/2/library/stdtypes.html#typecontextmanager>`_
describes how that works.

The tl;dr version (but do go read the documentation to understand
more!) is that a context manager provides the methods ``__enter__`` and
``__exit__``, and it is these which do the work mentioned above. The the
file and thread-lock objects in Python already come as context managers,
and there are a number more.

We could write our own example of how to handle file opens (not needed
since the Python file object is already a context manager) just to show
what a context manager looks like::

    class File():
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode

        def __enter__(self):
            self.open_file = open(self.filename, self.mode)
            return self.open_file

        def __exit__(self, *args):
            self.open_file.close()

    with File("foo.txt", "w") as outfile:
        outfile.write('foo')

Decorated Generators as Context Managers
========================================

We can of course write context managers in the style just shown, but often
it's easier to write a generator function, which we can then decorate
with syntax that will intsruct Python to turn it into a context manager.
The decoration is ``@contextlib.contextmanager`` (you can shorten that based
on the way you import), and what happens is the code before the "yield"
statement is turned into the ``__enter__`` method while the code after it
is turned into the ``__exit__`` method.

Let's show how this works with a somewhat practical example: timing an
operation via a context manager. Python already provides a very nice
timing module (timeit), but using it in the manner of this example (IMHO)
makes for nice readable code. The "wrapping" behavior of the context
manager doesn't have to be limited to critical code sections. Timing
code fits the model too: the "setup" is capturing a timestamp before
the context block runs; the "teardown" is capturing a timestamp after
it has completed, and then computing the difference (in the example we
also print out the result).

Here is a timing context manager in class form, plus some code to do
something we can time (fetching a URL)::

    from timeit import default_timer
    import requests

    class Timer(object):
        def __init__(self):
            self.timer = default_timer

        def __enter__(self):
            self.start = self.timer()
            return self

        def __exit__(self, *args):
            end = self.timer()
            self.elapsed_secs = end - self.start
            self.elapsed = self.elapsed_secs * 1000 # millisecs
            print 'elapsed time: %f ms' % self.elapsed

    url = 'https://github.com/timeline.json'
    with Timer():
        r = requests.get(url)

Running this, you might get something like::

    elapsed time: 375.089169 ms

Rewriting it into decorated-generator form::

    from timeit import default_timer
    import requests
    from contextlib import contextmanager

    @contextmanager
    def Timer():
        start = default_timer()
        yield
        elapsed_secs = default_timer() - start
        elapsed = elapsed_secs * 1000 # millisecs
        print 'elapsed time: %f ms' % elapsed

    url = 'https://github.com/timeline.json'
    with Timer():
        r = requests.get(url)

and this version works the same way as the previous one.

Context managers have very appealing applications in testing, where
there may be many test cases that each have lots of setup and teardown.
It's usually important that individual tests are isolated, so that running
one test does not impact the results of a future test; having a teardown
phase that runs reliably even if the test case went badly wrong is very
appealing. Since Python 2.7 (and thus all Python 3 versions), context
managers are composable - that is you can have combinations of multiple
setup and teardown steps, which can even feed into each other, like::

    with a(x, y) as A, b(A) as C:

Hopefully this post will have shown some of the uses of the "with"
statement.  As always, there are more goodies, only need to do a little
more digging!
