# =============================================================================
# Task 3: Encapsulation with Access Control
# =============================================================================
# Objective:
#   - Define a BankAccount class with a PRIVATE attribute __balance
#   - Provide public methods: deposit(), withdraw(), and get_balance()
#   - Enforce data integrity by controlling ALL access through these methods
#
# Key Concepts:
#   - Encapsulation: bundling data (attributes) and the methods that operate
#     on that data inside one class, while restricting direct outside access.
#   - Private attributes (__ double underscore): Python applies "name mangling",
#     renaming __balance to _BankAccount__balance internally. This makes
#     accidental external access very difficult, signaling "hands off".
#   - Public methods act as a controlled interface (a "gate") to the private
#     data — all reads and writes go through validation logic here, not
#     directly on the attribute from outside the class.
# =============================================================================


class BankAccount:

    def __init__(self, owner, initial_balance=0.0):
        """
        Constructor sets up the account with an owner name and starting balance.

        'owner' is a regular public attribute — it's fine to read externally.

        '__balance' uses the double-underscore prefix, making it PRIVATE.
        Python internally renames it to '_BankAccount__balance', so any code
        outside this class that tries to access obj.__balance gets an
        AttributeError — the balance can only be read or changed through
        the public methods defined below.

        initial_balance defaults to 0.0 if not provided, but we still run it
        through the same validation logic used by deposit() to reject bad input
        from the very start (e.g. someone passing a negative opening balance).
        """
        self.owner = owner  # Public: account holder's name

        # Initialize private balance to 0, then use deposit() to apply the
        # opening amount — this reuses validation logic rather than duplicating it.
        self.__balance = 0.0
        if initial_balance > 0:
            self.deposit(initial_balance)
        elif initial_balance < 0:
            print("Warning: Initial balance cannot be negative. Starting at $0.00.")

    # -------------------------------------------------------------------------
    # Getter Method — Controlled Read Access
    # -------------------------------------------------------------------------
    def get_balance(self):
        """
        The ONLY sanctioned way to read __balance from outside the class.

        Returning a value (rather than exposing the attribute directly) means
        we could add logic here later — e.g. rounding, formatting, logging —
        without changing any code that calls get_balance().
        """
        return self.__balance

    # -------------------------------------------------------------------------
    # Public Methods — Controlled Write Access
    # -------------------------------------------------------------------------
    def deposit(self, amount):
        """
        Adds 'amount' to __balance after validating the input.

        Encapsulation benefit: the rule "deposits must be positive" lives HERE,
        once, inside the class. External code can never bypass it by writing
        directly to __balance.
        """
        if amount <= 0:
            # Guard clause: reject invalid input before touching the balance
            print(f"  Deposit failed: amount must be positive (got ${amount:.2f}).")
            return  # Exit early — __balance is unchanged

        self.__balance += amount
        print(f"  Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")

    def withdraw(self, amount):
        """
        Deducts 'amount' from __balance after two validation checks:
            1. Amount must be positive (can't withdraw $0 or a negative value).
            2. Sufficient funds must exist (no overdrafts allowed).

        Both rules are enforced here and nowhere else — callers simply call
        withdraw() and trust the class to handle the rules correctly.
        """
        if amount <= 0:
            print(f"  Withdrawal failed: amount must be positive (got ${amount:.2f}).")
            return

        # Sufficient funds check — compare against the private attribute
        # (accessible here because we're INSIDE the class)
        if amount > self.__balance:
            print(f"  Withdrawal failed: insufficient funds. "
                  f"(Requested: ${amount:.2f} | Available: ${self.__balance:.2f})")
            return

        self.__balance -= amount
        print(f"  Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}")

    def __str__(self):
        """
        __str__ defines the human-readable string representation of the object.
        Called automatically by print(account) or str(account).
        """
        return f"BankAccount(owner='{self.owner}', balance=${self.__balance:.2f})"


# =============================================================================
# --- Demo / Test ---
# =============================================================================

print("=== Opening Account ===")
account = BankAccount(owner="Alice", initial_balance=500.00)
print(account)  # Calls __str__

print()
print("=== Valid Deposit ===")
account.deposit(250.00)

print()
print("=== Valid Withdrawal ===")
account.withdraw(100.00)

print()
print("=== Insufficient Funds ===")
account.withdraw(1000.00)  # Should be rejected — balance is only $650.00

print()
print("=== Invalid Inputs ===")
account.deposit(-50.00)    # Negative deposit — should be rejected
account.withdraw(0)        # Zero withdrawal — should be rejected

print()
print("=== Reading Balance via Getter ===")
print(f"  Current balance: ${account.get_balance():.2f}")

print()
print("=== Proving Private Access is Blocked ===")
# Attempting to access __balance directly from outside the class
try:
    print(account.__balance)  # Will raise AttributeError due to name mangling
except AttributeError as e:
    print(f"  AttributeError caught: {e}")

# However, Python's name-mangled attribute CAN be accessed if you know the
# internal name — this is by design (Python prefers convention over hard locks).
# This is shown here only to explain the mechanism, NOT as recommended practice.
print(f"  (Via mangled name, for educational purposes only): "
      f"${account._BankAccount__balance:.2f}")

print()
print("=== Final Account State ===")
print(account)
