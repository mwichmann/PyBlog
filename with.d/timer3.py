from timeit import default_timer
from contextlib import contextmanager

@contextmanager
def Timer():
    try:
        start = default_timer()
        yield 
    finally:
        elapsed_secs = default_timer() - start
        elapsed = elapsed_secs * 1000 # millisecs
        print 'elapsed time: %f ms' % elapsed



if __name__ == '__main__':
        # example:
    # 'HTTP GET' from requests module, inside timer blocks.
    # invoke the Timer context manager using the `with` statement.
    
    import requests
    
    url = 'https://github.com/timeline.json'
    
    with Timer():
        r = requests.get(url)
