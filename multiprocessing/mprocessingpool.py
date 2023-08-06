import multiprocessing
from multiprocessing import Pool
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

    num_processes = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=num_processes)

    result = pool.map(api_worker, ["task1", "task2"])

    pool.close()
    pool.join()

    end_time = time.time()
    print("Time taken: {}".format(end_time - start_time))
    print(result)
