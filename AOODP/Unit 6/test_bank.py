import unittest
import threading
from bank_account import BankAccount
from transaction_simulator import TransactionSimulator

class TestBankAccount(unittest.TestCase):
    """
    Unit tests for the BankAccount class covering functional and concurrency behaviour.
    """

    def test_deposit_increases_balance_by_correct_amount(self):
        account = BankAccount("ACC001", 100)
        account.deposit(50)
        self.assertEqual(account.get_balance(), 150)

    def test_withdraw_decreases_balance_by_correct_amount(self):
        account = BankAccount("ACC001", 100)
        account.withdraw(50)
        self.assertEqual(account.get_balance(), 50)

    def test_withdraw_raises_value_error_when_insufficient_funds(self):
        account = BankAccount("ACC001", 100)
        with self.assertRaises(ValueError):
            account.withdraw(150)

    def test_transfer_deducts_from_source_and_credits_target(self):
        account1 = BankAccount("ACC001", 100)
        account2 = BankAccount("ACC002", 100)
        account1.transfer(account2, 50)
        self.assertEqual(account1.get_balance(), 50)
        self.assertEqual(account2.get_balance(), 150)

    def test_transfer_raises_value_error_when_insufficient_funds(self):
        account1 = BankAccount("ACC001", 100)
        account2 = BankAccount("ACC002", 100)
        with self.assertRaises(ValueError):
            account1.transfer(account2, 150)

    def test_concurrent_deposits_produce_correct_final_balance(self): 
        account = BankAccount("ACC001", 0)
        thread1 = threading.Thread(target=lambda: [account.deposit(100) for _ in range(5)])
        thread2 = threading.Thread(target=lambda: [account.deposit(100) for _ in range(5)])
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        # If locking is broken, then one or more of the deposits would have failed. 
        self.assertEqual(account.get_balance(),1000) 

    def test_concurrent_mixed_transactions_never_produce_negative_balance(self): 
        account = BankAccount("ACC001", 0)
        sim = TransactionSimulator(account,100,100)
        sim.run()
        self.assertGreaterEqual(account.get_balance(), 0)

    def test_concurrent_bidirectional_transfers_do_not_deadlock(self): 
        account1 = BankAccount("ACC001", 100)
        account2 = BankAccount("ACC002", 100)
        # barrier needed to ensure that threads execute concurrently
        barrier = threading.Barrier(2)
        thread1 = threading.Thread(target=lambda: [barrier.wait(), account1.transfer(account2,50)])
        thread2 = threading.Thread(target=lambda: [barrier.wait(), account2.transfer(account1,50)])
        thread1.start()
        thread2.start()
        thread1.join(timeout=5)
        thread2.join(timeout=5)
        # If we deadlocked, the threads will still be alive
        self.assertFalse(thread1.is_alive())
        self.assertFalse(thread2.is_alive())

    def test_transfer_to_self_raises_value_error(self):
        """
        Ensures transferring money to the exact same account instance 
        fails immediately with a ValueError rather than causing a self-deadlock.
        """
        account = BankAccount("ACC001", 100)
        
        # The test runner executes the transfer within a context manager 
        # to assert that the specific exception is thrown.
        with self.assertRaises(ValueError):
            account.transfer(account, 50)
            
        # Verify that no funds were erroneously deducted during the aborted operation
        self.assertEqual(account.get_balance(), 100)
        

if __name__ == "__main__":
    unittest.main()
