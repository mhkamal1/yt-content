from multiprocessing import Process
import multiprocessing
import time

def api_worker(task):
    print("executing CPU intensive task ...")
    total = 0
    for i in range(10000):
        for j in range(10000):
            total += i * j
    return {task: total}

if __name__ == "__main__":

    start_time = time.time()

    # api_worker("task1")
    # api_worker("task2")

    # proc1 = Process(target=api_worker, args=("task1",))
    # proc2 = Process(target=api_worker, args=("task2",))

    # proc1.start()
    # proc2.start()

    # proc1.join()
    # proc2.join()

    end_time = time.time()
    
    print("Time taken: {}".format(end_time - start_time))





