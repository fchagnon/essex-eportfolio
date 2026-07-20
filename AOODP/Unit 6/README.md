# Unit 6: Concurrency and Parallelism in Object-Oriented Design

## Unit Topic

This unit covers concurrency and parallelism in an object-oriented
context: threads, processes, synchronization, and the common failure
modes, race conditions and deadlocks, that arise when multiple threads
share state. It was the module's sole summative coding exercise.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the basics of concurrency, including threads,
  processes, and synchronization.
- Apply object-oriented principles to write thread-safe code that avoids
  common concurrency issues.
- Identify and resolve common concurrency problems such as race
  conditions and deadlocks.
- Implement thread-safe code in Python through a practical exercise.

## Formative Assignment

*(Summative)*

Design and implement a thread-safe banking system supporting concurrent
deposits, withdrawals, and transfers across multiple accounts:

1. A `BankAccount` class with `deposit()`, `withdraw()`, and
   `get_balance()`, all thread-safe.
2. Synchronization via locks or semaphores to prevent race conditions.
3. A `TransactionSimulator` class simulating multiple users performing
   concurrent transactions using threads.
4. Deadlock prevention, particularly for transfers between two accounts.
5. Unit tests validating thread safety and correct final balances under
   concurrent load.

Full code: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%206

## Reading List

Quan, Nguyen (2022) *Advanced Python Programming*. 2nd edn. Birmingham:
Packt Publishing. Chapter 6, Section 2, and Chapter 7.

McDonald, J.C. (2023) *Dead Simple Python: Idiomatic Python for the
Impatient Programmer*. 1st edn. New York: No Starch Press. Chapters 17
and 20.

## Reflection

**Understanding concurrency basics.** `threading.Lock` was chosen over
`threading.Semaphore` because only one thread should ever modify a
balance at a time, a semaphore's permissiveness for multiple concurrent
accessors doesn't fit that constraint (Quan, 2022, ch.7). `User`
subclasses `threading.Thread` and overrides `run()`, applying the
Template Method pattern so each simulated user carries its own
encapsulated state (Sarcar, 2023, ch.1).

**Applying OOP principles to thread-safe code.** The lock is a private
instance attribute, so thread safety is guaranteed by the class itself
rather than depending on every caller to manage locking correctly.
`TransactionSimulator` receives its `BankAccount` via constructor
injection rather than creating one internally, the same Dependency
Inversion reasoning from Unit 2, applied here to make deterministic
testing possible: accounts can be constructed with known starting
balances and outcomes asserted exactly.

**Identifying and resolving race conditions and deadlocks.** `transfer()`
is the only method needing two locks simultaneously, and two concurrent
transfers in opposite directions will each hold one lock while waiting on
the other, satisfying Coffman's circular wait condition (Quan, 2022,
ch.6.2). The fix was resource ordering: locks are always acquired in
ascending order of Python object identity (`id()`), regardless of
transfer direction, which eliminates circular wait entirely. A
self-identified edge case, transferring an account to itself, would
acquire the same lock twice and deadlock immediately, guarded against
directly with an identity check that fails fast before any lock is
touched.

**Implementing and testing thread-safe code.** Nine unit tests split
functional correctness from concurrency-specific behaviour: a
deterministic concurrent-deposit test, a mixed-transaction stress test
asserting the balance never goes negative, and a deadlock test with a
timeout. `threading.Barrier` releases all simulated users at once,
maximising lock contention so the concurrency mechanisms are exercised
under genuine pressure rather than accidental sequential execution.

## Tutor Feedback and Response

**Feedback (70%, Distinction).** Strengths noted: appropriate
synchronization mechanisms, clearly articulated race conditions and
deadlocks, correct execution with deterministic concurrency scenarios,
clean and well-documented code following encapsulation and single
responsibility. Suggested improvements: a report with snippets and flow
diagrams; more detail on canonical lock ordering; explicit invariants
(conservation of total funds); requirement-to-feature traceability;
scalability analysis under high thread counts; improved error handling
for negative amounts; a pass/fail results table; a UML sequence diagram
of lock acquisition order; a run-instructions README; explicit inline
citation where external ideas informed the design.

**My response.** This feedback matched exactly how I felt about the
submission at the time. I wasn't trying to build a production system, and
that scoping was deliberate, but I should have demonstrated more explicit
awareness of what those limits were and named them directly, rather than
leaving it implicit. Notably, I addressed this specific gap in the very
next assignment: Unit 7's authentication system explicitly calls out its
own production limitations (in-memory lockout state not persisting across
restarts or scaling across server instances) as a named trade-off, rather
than leaving it unstated. That progression, internalizing this piece of
feedback and applying it unprompted one unit later, is itself a concrete
example of feedback translating into a changed habit, not just an
acknowledged critique.
