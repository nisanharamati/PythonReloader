PythonReloader
==============

Short sample of reloading new code on the fly directly into the active runtime loop of a worker (e.g. the kind you would have consuming a stream in real-time) by using the imp module.

run reloader/processworker.py or reloader/threadworker.py directly.


In a real-world application you should probably add some checks and guards against replacing your runtime function with one that breaks, or fails a unit test and all that jazz.
