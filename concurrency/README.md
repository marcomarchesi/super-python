# Multiprocessing

## Basic
- use of `Pool` as a context manager for **Data Parallelism**

```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == "__main__":
    with Pool(5) as pool:
        print(pool.map(f, [1, 2, 3]))
```

## Processes
- use of `Process` to spawn a process 

```python
from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('Alice',))
    p.start()
    p.join()
```

- `Process` is more efficient than `Pool` for a limited set of tasks that need to run longer. `Pool` waits for I/O operations to complete so it's more suitable if they are quick.

## Exchanging objects between Processes
- `Queue` is process safe
- put and get messages

```python
from multiprocessing import Process, Queue

def f(q):
    q.put(['hello', 'world']) 

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

- `Pipe` runs a duplex connection

```python
from multiprocessing import Process, Pipe

def f(connection):
    connection.send(['hello', 'world']) 
    connection.close()

if __name__ == '__main__':
    # the two ends of the Pipe
    parent_connection, child_connection = Pipe()
    p = Process(target=f, args=(child_connection,))
    p.start()
    print(parent_connection.recv())
    p.join()
```

## Sync between processes
- TODO
- also `Client` and `Listener` by doing
```python
from multiprocessing.connection import Client, Listener
```
and using `recv()` and `send()` to receive and send data

- difference between Pool.map and Pool.apply (and async versions)
- use messages for communication between processes rather than synchronisation primitives like locks.
- choose between `Pipe()` and `Queue()`

# Threading
- lock: acquire and release but you can have them implicitly in a context manager
- in threading: `map()` vs `submit()`. Map accepts an iterable as argument
-  **multiprocessing** is a form of **parallelism**, which is a form of **concurrency**, like **threading**
- **Deadlock** happens if a thread doesn't release the lock
- use a Pipeline to solve a Producer/Consumer problem
    -- but only one data at the time
    --> better with a Queue
- use a Queue and Event sync mechanism (as in `producer_consumer.py`)
- not easy to debug in general, try for example to forget to `import random` from the script above
- Threading objects
    `threading.Semaphore` used to protect resources, it's atomic (it cannot be interrupted)
    `threading.Timer` used for running functions with a delay on a new thread
    `threading.Barrier` it forces sync between a number of threads