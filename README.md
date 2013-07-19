PythonReloader
==============

Short sample of reloading new code on the fly directly into an active runtime loop by using the imp module.

run reloader/processworker.py or reloader/threadworker.py directly.


In a real-world application you should probably add some checks and guards against replacing your runtime function with one that breaks, or fails a unit test and all that jazz.
