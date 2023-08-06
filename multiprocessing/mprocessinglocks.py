import multiprocessing
from multiprocessing import Value

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        
    def deposit(self, amount, lock):
        # lock.acquire()
        with lock:
            print(f"Depositing {amount}")
            self.balance += amount
            print(f"New balance after deposit: {self.balance}")
        # lock.release()
if __name__ == "__main__":
    account = BankAccount(balance=1000)

    # Simulate multiple transactions using processes
    processes = []

    lock = multiprocessing.Lock()

    process1 = multiprocessing.Process(target=account.deposit, args=(100, lock))
    process2 = multiprocessing.Process(target=account.deposit, args=(100, lock))
    
    processes.append(process1)
    processes.append(process2)
    
    process1.start()
    process2.start()

    for process in processes:
        process.join()

    print("Final balance:", account.balance)
