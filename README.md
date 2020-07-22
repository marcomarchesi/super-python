# python-python
All I need on Python

[Coding Style](#Coding-Style)  
[Truth Value Testing](#Truth-Value-Testing)  
[String vs Bytes](#Strings-vs-Bytes)  
[Threading](#Threading)
[Functions](#Functions)  


## Coding Style
- to follow PEP8

## Truth Value Testing
- all objects are true by default apart empty lists, dictionaries and sets, `None` and `False` (of course)

## Strings vs Bytes
- use `byte_data.decode('utf-8)` to convert to `string`
- use `string_data.encode()` to convert to bytes


## Threading
- multiple processes run and share the same Python Interpreter (because of Global Interpreter Lock)
- they run in turns, not concurrently, at least on CPython (standard interpreter)
- CPython is bound on GIL
- When to use it:
1. if the task needs to wait long for external resources or events
2. to simplify design

```python
import threading
import time


def thread_function(name):
    print('hello world, thread {}'.format(name))
    time.sleep(2)
    print('hello world')


if __name__ == "__main__":
    
    x = threading.Thread(target=thread_function, args=(1,))
    # start the thread
    x.start()
    # wait for the thread to finish
    x.join()
    print('it''s over')
```

- `Daemon` threads run in background and they are killed once the main program is over.

```python
x = threading.Thread(target=thread_function, args=(1,), daemon=True)
```

- `.join()` makes the main thread waits for the secondary thread to complete
- threads can run in an unpredictable order, decided by the OS
- to instance multiple threads we can use `ThreadPoolExecutor`:

```python
import concurrent.futures

# [rest of code]

if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))  # instancing three threads and join each of them
```

- [ALERT] `ThreadPoolExecutor` can hide exceptions raised from a thread, for example if we pass an argument to a thread with zero arguments.
- **Race conditions** happen when two or more threads share data
- ** Locks ** help synchronising threads

## Functions
```python
def do_something(*args, **kwargs):  # positional and named arguments
    pass
```

