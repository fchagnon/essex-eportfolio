# Unit 6 Assignment: Thread-Safe Banking System

## Learning Outcomes

- Understand and implement secure coding practices in software development.
- Apply advanced object-oriented principles to solve complex software problems.

## Assignment Question

You are tasked with designing and implementing a thread-safe banking system that allows multiple users to perform transactions (e.g., deposit, withdraw, and check balance) concurrently. The system must ensure that all operations are thread-safe and avoid common concurrency issues such as race conditions and deadlocks.

## Requirements

### 1. Bank Account Class

Create a `BankAccount` class with the following attributes:

- `account_number` (unique identifier for the account)
- `balance` (current balance of the account)

Implement the following methods:

- `deposit(amount)`: Adds the specified amount to the balance.
- `withdraw(amount)`: Deducts the specified amount from the balance (if sufficient funds are available).
- `get_balance()`: Returns the current balance.

### 2. Thread Safety

Ensure that all methods in the `BankAccount` class are thread-safe. Use synchronisation mechanisms such as locks or semaphores to prevent race conditions.

### 3. Transaction Simulation

- Create a `TransactionSimulator` class that simulates multiple users performing transactions on the same bank account concurrently.
- Each user should perform a series of deposits and withdrawals.
- Use threads to simulate concurrent transactions.

### 4. Deadlock Prevention

Ensure that your implementation avoids deadlocks. For example, if two users are trying to transfer money between accounts, the system should handle this without causing a deadlock.

### 5. Testing and Validation

- Write unit tests to validate that the system is thread-safe and handles concurrent transactions correctly.
- Simulate scenarios where multiple users are performing transactions simultaneously and verify that the final balance is correct.

## Assignment Criteria

1. **Knowledge and understanding of the topic/issues under consideration (30%)**
   How well have you achieved the specifications/requirements of the given task? Have you completed all the required testing? Is the testing thorough and well organised? Is there accompanying documentation (which includes comments)? Does it provide an effective evaluation of the code/program?

2. **Application of knowledge and understanding (30%)**
   Does your code/program execute correctly with minimal errors? Is this an efficient solution, easy to understand and maintain?

3. **Structure and Presentation (as detailed in the assessment guidance) (30%)**
   How well have you followed the correct standards/best practice for your coding/programming exercise? Is the accompanying documentation (which includes comments) well-written? Have all other structural tasks been fully achieved?

4. **Academic integrity (10%)**
   Have you demonstrated the required integrity in your submission, in line with institutional guidelines? For example, minimal use of sections of code from lecture casts/unit notes and source clearly stated in the comments.
