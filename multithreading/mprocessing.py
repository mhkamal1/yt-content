import multiprocessing
from multiprocessing import Process
import time

def api_worker():
    print("executing CPU intensive task ...")
    total = 0
    for i in range(10000):
        for j in range(10000):
            total += i * j
    return total

if __name__ == "__main__":
    # numbers = [1, 2, 3, 4, 5]
    start_time = time.time()

    for _ in range(2):
        api_worker()

    # for _ in range(2):
    #     procs=[]
    #     proc = Process(target=api_worker)
    #     procs.append(proc)
    #     proc.start()

    # for proc in procs:
    #     proc.join()

    end_time = time.time()
    print("Time taken: {}".format(end_time - start_time))

    ############

    # # Create a multiprocessing Pool with the number of available CPU cores
    # num_processes = multiprocessing.cpu_count()

    # pool = multiprocessing.Pool(processes=num_processes)

    # # Map the calculate_square function to each number in the list using the Pool
    # pool.map(calculate_square, numbers)

    # # Close the Pool to release resources
    # pool.close()
    # pool.join()
