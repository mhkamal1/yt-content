import threading
import time

def api_worker():
    print("executing CPU intensive task ...")
    total = 0
    for i in range(10000):
        for j in range(10000):
            total += i * j
    return total

start_time = time.time()

# for _ in range(2):
#     api_worker()

thread1 = threading.Thread(target=api_worker)
thread2 = threading.Thread(target=api_worker)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

end_time = time.time()

print("Time taken: {}".format(end_time - start_time))

