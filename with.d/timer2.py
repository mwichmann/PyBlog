from timeit import default_timer


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



if __name__ == '__main__':
        # example:
    # 'HTTP GET' from requests module, inside timer blocks.
    # invoke the Timer context manager using the `with` statement.
    
    import requests
    
    url = 'https://github.com/timeline.json'
    
    with Timer():
        r = requests.get(url)
