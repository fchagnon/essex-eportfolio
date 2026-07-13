import threading
import random

class User(threading.Thread):
    """
    A user (thread) within the transaction simulator tha that performs transactions

    """
    def __init__(self, account, barrier, num_transactions):
        """
	Initializes a new user thread within our simulator
        
        Args: 
            account: the BankAccount number
            barrier: the barrier object that the user waits on before executing
            num_transactions: the number of transactions this thread instance will perform
        """
        super().__init__()
        self._account = account
        self._barrier = barrier
        self._num_transactions = num_transactions

    def run(self):
        """
        The user's main execution function
        """
        # This barrier is in place to ensure all threads start at the same time.
        # Without this, it's possible (however unlikely) that our threads execute
        # entirely in sequence and we're not actually simulating concurrency. 
        self._barrier.wait()
        
        for _ in range(self._num_transactions):
            amount = random.randint(1, 50)
            if random.choice([True, False]):
                self._account.deposit(amount)
            else:
                try:
                    self._account.withdraw(amount)
                except ValueError:
                    pass


class TransactionSimulator:
    """
    Simulates multiple concurrent transactions to a bank account in order to stress
    test concurrency
    """
    def __init__(self, account, num_users, num_transactions):
        """
        Initiatializes the transaction simulator instance

        Args: 
             account: The BankAccount instance we want to hammer away at
             num_users: The number of concurrent users (threads) we will run in parallel
             num_transactions: The number of transactions each user will be executing
        """
        self._account = account
        self._num_users = num_users
        self._num_transactions = num_transactions

    def run(self):
        """
        The simulator's main execution function
        """
        # Establish a barrier with an internal counter for the number of threads we're creating. 
        # No thread starts actually executing until all threads are in a ready state. 
        barrier = threading.Barrier(self._num_users)

        users = [
            User(self._account, barrier, self._num_transactions)
            for _ in range(self._num_users)
        ]
        # Instantiate the threads
        for user in users:
            user.start()

        # Wait for the threads to complete
        for user in users:
            user.join()
