import threading
class BankAccount:
    """
    Unit 6 Assignment. A thread-safe bank account that supports 
    concurrent deposits, withdrawals, and transfers.
    """
    def __init__(self, account_number, initial_balance=0):
        """
        Initialises a new BankAccount instance.

        Args:
            account_number: Unique identifier for the account.
            initial_balance: Starting balance, defaults to 0.
        """
        self._account_number = account_number
        self._balance = initial_balance
        self._lock = threading.Lock()

    def get_account_number(self):
        """
        Returns: the account number of the BankAccount instance
        """
        return self._account_number

    def get_balance(self):
        """
        Returns: the balance of the BankAccount instance. 
        """
        with self._lock:
            # lock the account for reading to protect against concurrent modifications of the amount
            # by parallel threads executing deposits and withdrawals
            return self._balance

    def deposit(self, amount):
        """
        Deposits an amount into the BankAccount instance. 

        Args:
            amount: the amount to deposit
        Returns: 
            True if the deposit was successful
        """
        with self._lock:
            # lock the account for writing to protect against concurrent reads or writes on the amount
            # by parallel threads attempting to execute deposits and withdrawals
            self._balance += amount
            return True

    def withdraw(self, amount):
        """
        Withdraws an amount into the BankAccount instance. 

        Args:
            amount: the amount to withdraw

        Raises: 
            ValueError: if the withdrawal amount is greater than the balance
 
        Returns: 
            True if the withdrawal was successful
        """
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
            else:
                raise ValueError("Insufficient funds")

    def transfer(self, target_account, amount):
        """
        Transfers an amount from a source BankAccount to a target BankAccount instance

        Args:
            target_account: the target BankAccount instance (where "self" represents the source account)
	    amount: the amount being transferred between accounts

        Raises: 
            ValueError: if the source account and the target account are the same
            ValueError: if the source account has insufficient funds for the transfer

        Returns: 
            True if the transfer was successful
        """
        # Deadlock protection -- ensure that the source account and target account are not the
        # same. Otherwise the program will acquire one lock, and then be deadlocked waiting for
        # a lock on the same account. 
        if self is target_account:
            raise ValueError("Cannot transfer funds to the same account.")

        # Deadlock protection. Always lock the lower account number first, then the higher one. 
        # Ensures that a concurrent thread transferring the opposite direction won't be caught
        # holding the lock we need, and waiting for the one we have. 
        if id(self) < id(target_account):
            lock_a = self._lock
            lock_b = target_account._lock
        else:
            lock_a = target_account._lock
            lock_b = self._lock

        # Because we have our own locks in place, we actually can't use self.withdraw() 
        # and target_account.deposit() methods to execute the transfer. These methods would
        # attempt locks of their own, and we'd be deadlocked. So instead we need to write 
        # directly to the private instance variable. (Not exactly production grade)
        with lock_a, lock_b:
            if self._balance >= amount:
                self._balance -= amount
                target_account._balance += amount
                return True
            else:
                raise ValueError("Insufficient funds")
