'''
multiprocessing_lock.py
'''

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