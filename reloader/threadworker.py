import threading
import Queue
import time
import loader

# a basic iterative worker that executes the same function in a continuous
# loop.
# We will be replacing the function it's executing on the fly.
class Worker(threading.Thread):
    def __init__(self, filename='func1.py', function='func'):
        # initialize the thread
        super(Worker, self).__init__()
        
        # set stop parameters...
        self._event = threading.Event()
        self._out = Queue.Queue()
        # assign the function to an instance attribute
        self.replace_function(filename, function)
        
    # replace the function instance attribute with a new function
    def replace_function(self, filename, function='func'):
        self._func = loader.load_func(filename, function)
        print 'function replaced:', filename, function
    
    # use a queue to get results in real time from the worker
    # let the parent deal with the no-data case.
    def get(self):
        try:
            return self._out.get_nowait()
        except Queue.Empty:
            return None
    
    def run(self):
        while not self._event.is_set():
            self._out.put(self._func(time.time()))
            time.sleep(1)
    
    def stop(self):
        self._event.set()



## test the class
if __name__ == '__main__':
    seconds = 3
    # create worker instance
    w = Worker()
    # start it...
    w.start()
    # sleep for a buncha time
    # use a chunkated sleeper...
    # print a result if one is available.
    _t = time.time()+seconds
    while time.time() < _t:
        time.sleep(0.1)
        o = w.get()
        if o is not None:
            print o
    o = w.get()
    if o is not None:
        print o
    
    
    # tell the worker to reload its function
    w.replace_function('func2.py', 'func')
    
    # repeat the sleep period
    _t = time.time()+seconds
    while time.time() < _t:
        time.sleep(0.1)
        o = w.get()
        if o is not None:
            print o
    o = w.get()
    if o is not None:
        print o
    
    # stop worker.
    w.stop()