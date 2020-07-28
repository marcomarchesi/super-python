'''
threading_semaphore.py
'''
from threading import Condition, Thread, current_thread, Semaphore
import logging
import time

def consumer(s):
    t = current_thread()
    logging.info("Consumer %s" % t)
    with s:
        time.sleep(1) # give some delay to appreciate the threading effects
        logging.info("Resource available for %s" % t)

def producer(s):
    t = current_thread()
    logging.info("Producer %s" % t)
    with s:
        time.sleep(1) # give some delay to appreciate the threading effects
        logging.info("Making resource available")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    condition = Condition()
    semaphore = Semaphore(2) # set the max capacity to 2
    c1 = Thread(target=consumer, args=(semaphore,))
    c2 = Thread(target=consumer, args=(semaphore,))
    c3 = Thread(target=consumer, args=(semaphore,))
    c4 = Thread(target=consumer, args=(semaphore,))
    p = Thread(target=producer, args=(semaphore,))

    p.start()
    c1.start() # p and c1 acquire the lock
    c2.start()
    c3.start() # c2 and c3 acquire the lock
    c4.start() # c4 acquires the lock
    
