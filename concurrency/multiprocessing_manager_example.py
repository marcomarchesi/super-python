'''
multiprocessing_manager_example.py
'''
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
    # create a list to share between processes
    shared_list = manager.list()

    # processes
    process1 = Process(target=worker1, args=[shared_list])
    process2 = Process(target=worker2, args=[shared_list])
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    # results
    print(shared_list) #[1, 3, 2, 4] but [1, 2, 3, 4] if we uncomment time.sleep(1) 
