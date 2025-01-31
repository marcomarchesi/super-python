# Concurrency

- Pre-emptive multitasking (1 CPU): the OS switches between tasks (time-sharing) `threading`
- Cooperative multitasking (1 CPU): the tasks decide when to give up control. They run concurrently on a single thread as coroutines. `asyncio`
- Multiprocessing (multiple CPUs): the processes run on different processors `multiprocessing`

## Threading

- multiple processes run and share the same Python Interpreter (because of Global Interpreter Lock)
- they run in turns, not concurrently, at least on CPython (standard interpreter)
- CPython is bound on GIL
- When to use it:
1. if the task needs to wait long time for external resources, or we want to run multiple I/O bound tasks simultaneously.
Example: [web_scraper.py](web_scraper.py)
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
- **Race conditions** happen when two or more threads share data. Example in [race_condition.py](race_condition.py)
- ** Locks ** help synchronising threads
- lock: acquire and release but you can have them implicitly in a context manager
- in threading: `map()` vs `submit()`. Map accepts an iterable as argument
- **Deadlock** happens if a thread doesn't release the lock
- use a Pipeline to solve a Producer/Consumer problem
    -- but only one data at the time
    --> better with a Queue
- use a Queue and Event sync mechanism (as in `producer_consumer.py`)
- not easy to debug in general, try for example to forget to `import random` from the script above
- Threading objects
    `threading.Semaphore` used to protect resources, it's atomic (it cannot be interrupted) by acquire/release it
    `threading.Timer` used for running functions with a delay on a new thread
    `threading.Barrier` it forces sync between a number of threads

- `threading.Event`. One thread signals an event and other threads wait for it. See the example in [producer_consumer.py](producer_consumer.py)

- `threading.Condition`. Conditions are like an Event + Lock. So multiple threads wait for an event (a condition in this case) to become true and then they have access to some exclusive shared resources (like it happens with a lock).


## Multiprocessing
-  **multiprocessing** is a form of **parallelism**, which is a form of **concurrency**, like **threading**

### Basic
- use of `Pool` as a context manager for **Data Parallelism**

```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == "__main__":
    with Pool(5) as pool:
        print(pool.map(f, [1, 2, 3]))
```

### Processes
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

### Exchanging objects between Processes
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

### Sync between processes
- TODO
- also `Client` and `Listener` by doing
```python
from multiprocessing.connection import Client, Listener
```
and using `recv()` and `send()` to receive and send data

- difference between Pool.map and Pool.apply (and async versions)
- use messages for communication between processes rather than synchronisation primitives like locks.
- choose between `Pipe()` and `Queue()`: `Pipe` connects two processes, while `Queue` can connect multiple Producers and Consumers

### Manager
- we use `Manager` to share data between processes which can run also on different machines and are connected over a network.
- 

- Example:
```python
from multiprocessing import Manager, Process
import time


def worker1(l):
    l.append(1)
    # time.sleep(1)
    l.append(3)

def worker2(l):
    l.append(2)
    # time.sleep(1)
    l.append(4)

if __name__ == "__main__":
    # create the manager
    manager = Manager()
    # create a list to share between processes. We can share also dictionaries
    shared_list = manager.list()

    # processes
    process1 = Process(target=worker1, args=[shared_list])
    process2 = Process(target=worker2, args=[shared_list])
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    # results
    print(shared_list) #it can be out-of-order but if we uncomment time.sleep(1) we force order
```

### Event
- `multiprocessing.Event` can be used to make processes wait for events and sync the data (otherwise out of order by default).
- Example with Event and Manager [multiprocessing_event_example.py](multiprocessing_event_example.py)

```python
from multiprocessing import Manager, Process, Event
import logging


def worker1(l, e):
    # e.wait()
    l.append(1)
    l.append(2)
    logging.info("worker 1 is complete")

def worker2(l, e):
    e.wait() # this worker waits for the event to be set
    l.append(3)
    l.append(4)
    logging.info("worker 2 is complete")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # create the manager
    event = Event()
    manager = Manager()
    # create a list to share between processes
    shared_list = manager.list()

    # processes
    process1 = Process(target=worker1, args=[shared_list, event])
    process2 = Process(target=worker2, args=[shared_list, event])
    process1.start()
    process2.start()
    # process 1 can complete without waiting for any event while process 2 is blocked by the event
    process1.join()
    print(shared_list) #[1, 2] from process 1

    # set the event that unblocks process 2
    event.set() 

    process2.join()
    # results
    print(shared_list) #[1, 2, 3, 4] in order
```
- Example by using a `Queue` that demonstrates how to put and get values in the right order, synchronised by an `Event`. [multiprocessing_queue_event_example.py](multiprocessing_queue_event_example.py)
- alternatives: not a `Queue` as we put/get the values from it. Let's try a `Lock` applied on a list

### Lock
- another way to synchronising is using `Lock`
- Example [multiprocessing_lock.py](multiprocessing_lock.py)
```python
from multiprocessing import Process, Lock
import time

def worker(l, i):
    l.acquire()
    # time.sleep(2) to simulate the order we acquire with lock
    try:
        print("Hello World", i)
    finally:
        l.release()
        pass

if __name__ == "__main__":
    lock = Lock()
    for i in range(10):
        Process(target=worker, args=(lock, i)).start()
```


## Async IO
- let's turn all the tasks into coroutines, prefacing all function with `async`.
- it works faboulously in networking situations
- it scales better than threading

- a **coroutine** is a function that can be paused to make run other coroutines
- for **future/task** use `ensure_future()` if we need to retrieve the results
- tasks are futures, `Task` is a subclass of `Future`
- a **task** is an object wrapped around a coroutine and made run in the event loop
- from [GvR's answer](https://github.com/python/asyncio/issues/477): use `create_task()` if we need to create a `Task` from a coroutine. `ensure_future()` is required if we want to retrieve a `Future` as return. 
**STILL A BIT CONFUSING**

- in summary:
    1. run the eventloop with `asyncio.run(main())`
    2. create the tasks on `main()` and gather them


- Examples:
    - [Basic](async_io_example.py)
    - [Web Scraper](asyncio_web_scraper.py)

 

