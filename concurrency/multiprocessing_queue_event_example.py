'''
multiprocessing_queue_event_example.py
'''
from multiprocessing import Process, Event, Queue
import logging


def worker1(q, e):
    q.put(1)
    q.put(2)
    logging.info("worker 1 is complete")

def worker2(q, e):
    e.wait() # this worker waits for the event to be set
    q.put(3)
    q.put(4)
    logging.info("worker 2 is complete")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    event = Event()
    # create a queue
    queue = Queue(maxsize=100)

    # processes
    process1 = Process(target=worker1, args=[queue, event])
    process2 = Process(target=worker2, args=[queue, event])
    process1.start()
    process2.start()
    # process 1 can complete without waiting for any event while process 2 is blocked by the event
    process1.join()
    print(queue.get()) #1 from the queue
    # set the event that unblocks process 2
    event.set() 

    process2.join()
    # results
    print(queue.get()) #2 from the queue, as expected the event mechanism forced to put values in order
    queue.close()
   
