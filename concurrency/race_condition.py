'''
race_condition.py
'''

import concurrent.futures
import threading
import logging
import time

class FakeDatabaseWithLock:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        current_thread = threading.current_thread()
        print("%s starting update" % (current_thread))
        # self._lock.acquire()
        #solution with context manager that prevents to forget to release the lock
        with self._lock: #other threads need to wait until the lock holder release it
            local_copy = self.value
            local_copy += 1
            time.sleep(0.01) #this makes the thread pauses, allowing other threads to run
            self.value = local_copy
        # self._lock.release()
        print("%s completed update" % (current_thread))

class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        current_thread = threading.current_thread()
        print("%s starting update" % (current_thread))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.01) #this makes the thread pauses, allowing other threads to run
        self.value = local_copy
        print("%s completed update" % (current_thread))

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    database = FakeDatabaseWithLock()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # for index in range(3):
        #     executor.submit(database.update)
        executor.map(database.update, [i for i in range(3)])
    logging.info("Testing update. Ending value is %d.", database.value)




