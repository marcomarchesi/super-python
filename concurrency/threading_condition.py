'''
threading_condition.py
'''
from threading import Condition, Thread, current_thread
import logging
import time

def consumer(cond):
    t = current_thread()
    logging.info("Consumer %s" % t)
    with cond:
        cond.wait()
        logging.info("Resource available")

def producer(cond):
    t = current_thread()
    logging.info("Producer %s" % t)
    with cond:
        logging.info("Making resource available")
        cond.notifyAll()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    condition = Condition()
    c1 = Thread(target=consumer, args=(condition,))
    c2 = Thread(target=consumer, args=(condition,))
    p = Thread(target=producer, args=(condition,))

    c1.start()
    # time.sleep(2)
    c2.start()
    # time.sleep(2)
    p.start()
    c1.join()
    c2.join()
    p.join()