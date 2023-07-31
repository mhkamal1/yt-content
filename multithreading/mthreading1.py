import threading
import time

def api_worker():
    while True:
        print(f"running...")
        time.sleep(1)        

def execute_stuff():
    print("executed!")

thread1 = threading.Thread(target=api_worker)
thread1.start()

execute_stuff()