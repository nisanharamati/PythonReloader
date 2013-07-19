import multiprocessing
import time
from Queue import Empty
import loader

# a basic iterative worker that executes the same function in a continuous
# loop.
# We will be replacing the function it's executing on the fly.
def _identity(x):
    return x

class Worker(multiprocessing.Process):
    def __init__(self, filename='func1.py', function='func'):
        # initialize the thread
        super(Worker, self).__init__()
        # set stop parameters...
        self._event = multiprocessing.Event()
        # with multiprocessing we need a queue or a pipe to communicate in real time
        self._out = multiprocessing.Queue()
        # function replacement queue
        self._new_func_queue = multiprocessing.Queue() # this guy takes a tuple of file path and function name!
        self.replace_function(filename, function)
    
    # replace the function instance attribute with a new function
    # this is not so simple for a Process, we need to pass the function somehow
    # and then signal that it's been passed
    def replace_function(self, filename, function='func'):
        self._new_func_queue.put((filename, function)) 
        print 'replaced function:', filename, function
    
    def get(self):
        try:
            return self._out.get_nowait()
        except Empty:
            return None
    
    def run(self):
        while not self._event.is_set():
            # test new func
            self._check_new_function()
            self._out.put(self._func(time.time()))
            time.sleep(1)
    
    def _check_new_function(self):
        if self._new_func_queue.qsize() > 0:
            _file, _func = self._new_func_queue.get()
            self._func = loader.load_func(_file, _func)
    
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
    w.join()