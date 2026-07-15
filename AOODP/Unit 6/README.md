# Unit 6: Concurrency and Parallelism in Python
### Thread-Safe Banking System
*Graded: 70% (Distinction)*

## Task

Implement a thread-safe BankAccount class supporting concurrent deposits,
withdrawals, and transfers, and a TransactionSimulator that stress-tests
the system under concurrent load.

## Artefacts

- **bank_account.py**: BankAccount class: deposit(), withdraw(),
  transfer(), all protected by threading.Lock.
- **transaction_simulator.py**: User (subclasses threading.Thread,
  overrides run()) and TransactionSimulator, which drives many concurrent
  users against a shared account using threading.Barrier.
- **test_bank.py**: 9 unit tests, split between functional correctness and
  concurrency-specific behavior.

```python
def transfer(self, target_account, amount):
    if self is target_account:
        raise ValueError("Cannot transfer funds to the same account.")

    if id(self) < id(target_account):
        lock_a = self._lock
        lock_b = target_account._lock
    else:
        lock_a = target_account._lock
        lock_b = self._lock

    with lock_a, lock_b:
        if self._balance >= amount:
            self._balance -= amount
            target_account._balance += amount
            return True
        else:
            raise ValueError("Insufficient funds")
```

## Design Decisions and Patterns

**Lock over Semaphore.** threading.Lock is used rather than
threading.Semaphore, since only one thread should ever modify the balance
at a time. A semaphore's permissiveness for multiple concurrent accessors
doesn't fit that constraint (Quan, 2022, ch.14).

**Encapsulation.** The lock is a private instance attribute, invisible to
callers. Thread safety is guaranteed by the class itself rather than
depending on callers to manage locking correctly. Python's privacy convention
is not enforced by the language, however: nothing prevents code from
bypassing the lock by directly manipulating _balance, which would be a
meaningful security concern in a production system (Quan, 2022, ch.14).

**Template Method Pattern.** User subclasses threading.Thread and
overrides run(), applying the Template Method pattern, where a parent
class defines an algorithm's skeleton and delegates specific behavior to
subclasses (Sarcar, 2023, ch.1). This was preferred over a plain target
function because each simulated user carries its own state, which benefits
from encapsulation within the object.

**Dependency Inversion.** TransactionSimulator receives its BankAccount
instance as a constructor argument rather than creating one internally
(Sarcar, 2023, ch.1), decoupling the simulator from the specific account it
operates on and making the system directly testable against accounts with
known starting balances.

## Concurrency and Deadlock Prevention

**Lock granularity in transfer().** transfer() manages its own locks
rather than delegating to deposit()/withdraw(), since both of those
methods acquire self._lock internally, delegating would cause the thread
to attempt acquiring a lock it already holds, resulting in reentrant
deadlock. This requires writing directly to _balance on both account
objects, a known and accepted trade-off between correctness and strict
encapsulation.

**Resource ordering.** transfer() is the only point where two locks must
be held simultaneously. Without intervention, two concurrent transfers in
opposite directions will each acquire one lock and wait indefinitely for the
other, satisfying Coffman's circular wait condition (Quan, 2022, ch.12). The
solution: locks are always acquired in ascending order of object identity
via id(), regardless of transfer direction, eliminating circular wait
entirely.

**Self-transfer guard.** A self-transfer would acquire the same lock twice
and deadlock immediately. Guarded against directly:

```python
if self is target_account:
    raise ValueError("Cannot transfer funds to the same account.")
```

**Deterministic stress testing.** TransactionSimulator uses
threading.Barrier to release all user threads simultaneously, maximising
lock contention and ensuring the locking mechanisms are exercised under
genuine concurrent pressure rather than accidental sequential execution.

## Testing

Nine tests, split between functional correctness (deposit/withdraw/transfer
behavior, insufficient-funds handling, self-transfer rejection) and
concurrency-specific behavior:
- **Concurrent deposits**: deterministic: two threads, five $100 deposits
  each against a zero balance, must always total $1000; any deviation
  signals a race condition.
- **Mixed transactions**: 100 simulated users against one account, balance
  must never go negative.
- **Deadlock test**: two threads performing opposite-direction transfers
  simultaneously, joined with a 5-second timeout; a thread still alive after
  the timeout has deadlocked.

```
test_concurrent_bidirectional_transfers_do_not_deadlock ... ok
test_concurrent_deposits_produce_correct_final_balance ... ok
test_concurrent_mixed_transactions_never_produce_negative_balance ... ok
test_deposit_increases_balance_by_correct_amount ... ok
test_transfer_deducts_from_source_and_credits_target ... ok
test_transfer_raises_value_error_when_insufficient_funds ... ok
test_transfer_to_self_raises_value_error ... ok
test_withdraw_decreases_balance_by_correct_amount ... ok
test_withdraw_raises_value_error_when_insufficient_funds ... ok
----------------------------------------------------------------------
Ran 9 tests in 0.028s
OK
```

## Limitations and Evaluation

Python's Global Interpreter Lock (GIL) ensures only one thread executes
bytecode at a time, meaning this implementation achieves concurrency but not
true parallelism (Quan, 2022, ch.15). For a banking system with brief,
largely IO-bound operations, this is unlikely to be significant in practice,
but the GIL does not substitute for application-level locking; threads still
interleave and race conditions remain possible without explicit locks.

Python's conventional (not enforced) encapsulation represents a genuine
security risk: nothing prevents code from directly manipulating _balance,
bypassing the lock entirely. threading.RLock throughout would allow
transfer() to safely delegate to deposit()/withdraw(), restoring full
encapsulation while eliminating the reentrant deadlock risk. A clear path
to improvement not taken here, in the interest of keeping the locking
strategy explicit.

This implementation demonstrates concurrency principles rather than
production-grade banking capabilities. A real system would require
persistent storage, transaction logging, rollback on failure,
authentication, and audit trails. The simplicity here is intentional,
allowing the concurrency mechanisms to be examined without production-grade
noise.

## Tutor Feedback

**Knowledge and understanding.** Evidence of banking requirements and
related theory is present; race conditions, concurrency, and deadlocks are
clearly articulated. Suggested additions: a report with snippets and flow
diagrams to aid understanding of the logic; more detail on canonical lock
ordering specifically; explicit invariants (e.g. conservation of total
funds) demonstrated alongside the tests; explicit mapping of each assignment
requirement to its implemented feature/test for full traceability; analysis
of scalability limits under very high thread counts.

**Application of knowledge and understanding.** Code executes correctly,
with clear evidence of deposits, withdrawals, and transfers across multiple
accounts; the TransactionSimulator produces deterministic, reproducible
concurrency scenarios. Noted as strong: deadlock-free behavior across
single- and two-account scenarios. Suggested additions: real-world features
such as transaction logging, rollback, or persistence; stress tests at much
larger scale (thousands of accounts/users).

**Structure and presentation.** Code is modular, clean, and well-documented,
with docstrings and precise comments aiding maintainability. Suggested
additions: pass/fail tables for test results; UML sequence diagrams showing
lock acquisition order; graphical performance summaries; a brief README with
run instructions and example output.

**Academic integrity.** Originality and integrity confirmed; design and
testing rationale clearly in the student's own words; references
demonstrate good research. Suggested improvement: note in code comments
specifically where external ideas (e.g. lock ordering strategy) were
informed by references, for complete transparency.

## Response to Feedback

This feedback matches exactly how I felt about the submission at the time,
I wasn't trying to build a production system, and that scoping was
deliberate, but I should have demonstrated more explicit awareness of what
those limits actually were and called them out directly, rather than
leaving it implicit in a general "Limitations and Evaluation" section.

Notably, I addressed this gap in the very next assignment: the Unit 7
authentication system explicitly calls out its own production limitations
(e.g. in-memory lockout state not persisting across restarts or scaling
across server instances) as a named trade-off, rather than leaving it
unstated. That progression, internalizing this specific piece of feedback
and applying it unprompted one unit later, is itself a concrete data point
for how feedback translated into a changed habit, not just an acknowledged
critique.

The more mechanical suggestions (a pass/fail results table, a UML sequence
diagram of lock acquisition order, explicit inline citation at the specific
lines implementing lock ordering, a run-instructions README) are separately
worth doing, since they were named across multiple feedback categories and
are straightforward additions rather than redesigns.

## References

McDonald, J. C. (2023) *Dead Simple Python: Idiomatic Python for the
Impatient Programmer*. 1st edn. New York: No Starch Press.

Quan, Nguyen (2022) *Advanced Python Programming*. 2nd edn. Birmingham:
Packt Publishing.

Sarcar, V. (2023) *Java Design Patterns: A Hands-On Experience with
Real-World Examples*. 3rd edn. Berkeley, CA: Apress.
