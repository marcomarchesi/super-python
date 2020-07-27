'''
multiprocessing_event_example.py
'''
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
   
