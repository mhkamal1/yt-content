import multiprocessing
from multiprocessing import Value, Array

class BankAccount:
    def __init__(self, balances):
        self.balances = Array("f", balances)

    def deposit(self, amounts, lock):
        lock.acquire()
        
        print(f"Depositing {amounts}")
        for i in range(len(amounts)):
            self.balances[i] += amounts[i]

        print(f"New balance after deposit: {self.balances[:]}")
        
        lock.release()

if __name__ == "__main__":
    account = BankAccount(balances=[100, 200, 300])

    # Simulate multiple transactions using processes
    processes = []
    lock = multiprocessing.Lock()
    # for _ in range(2):
    process1 = multiprocessing.Process(target=account.deposit, args=([100,100,100],lock))
    process2 = multiprocessing.Process(target=account.deposit, args=([100,100,100],lock))
    
    processes.append(process1)
    processes.append(process2)
    
    process1.start()
    process2.start()

    for process in processes:
        process.join()

    print("Final balance:", account.balances[:])
