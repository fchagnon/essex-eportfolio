# Unit 5: Behavioural Patterns
### Collaborative Discussion: Refactoring to the Strategy Pattern
*(Formative, collaborative discussion format)*

## Task

Analyze a simple payment-processing code snippet and refactor it using the
Strategy Pattern.

**Original code:**

```python
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            print(f"Processing credit card payment of ${amount}")
        elif payment_type == "paypal":
            print(f"Processing PayPal payment of ${amount}")
        elif payment_type == "bank_transfer":
            print(f"Processing bank transfer of ${amount}")
        else:
            raise ValueError("Invalid payment type")
```

## My Original Post

**1. Problems in the Current Implementation**

The existing PaymentProcessor class violates the Open/Closed Principle.
Every new payment type requires cracking open the class and adding another
elif branch, that's modification, not extension. The class also does too
much: it owns both the routing logic and the payment logic, making it
increasingly unwieldy as payment methods grow, which violates SRP as well.

**2. How the Strategy Pattern Improves the Code**

The Strategy Pattern fixes this by extracting each payment method into its
own class, all inheriting from a common abstract base (PaymentStrategy).
Adding a new payment type means adding a new class (extension), not another
elif block (modification). Changes here don't require changes there. The
codebase becomes genuinely modular, which scales nicely.

**3. Refactored Code**

```python
from abc import ABC, abstractmethod

# Abstract base class - broadcasting loud and proud that we're using the Strategy Pattern
# Any new payment type MUST implement the pay method. No exceptions.
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

# Concrete strategies - each payment type minds its own business
# Adding a new payment type means adding a new class, NOT touching existing code
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Processing credit card payment of ${amount}")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Processing PayPal payment of ${amount}")

class BankTransferPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Processing bank transfer of ${amount}")

class CryptoPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"WARNING: CryptoBro scammer detected. Processing crypto payment of ${amount}")

# PaymentProcessor doesn't know or care which payment type it's dealing with
# It just knows it has a strategy with a pay method. That's the whole contract.
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def process_payment(self, amount: float) -> None:
        self._strategy.pay(amount)

# Usage - PaymentProcessor has no idea what it's talking to, and that's the point
processor = PaymentProcessor(CreditCardPayment())
processor.process_payment(150.00)
processor.set_strategy(PayPalPayment())
processor.process_payment(75.50)
processor.set_strategy(CryptoPayment())
processor.process_payment(99.99)
```

**4. Benefits**

- **Readability**: no more nested elif chains to untangle
- **Modularity**: each payment type is self-contained
- **Stability**: adding CryptoPayment doesn't risk breaking CreditCardPayment
- **Maintainability**: no chain of dependencies triggered by a single modification
- **SOLID compliance**: open for extension, closed for modification, single responsibility preserved

## Peer Engagement

Replied to Reena's post, which implemented Strategy using a strategy_map
dictionary (payment_type string → strategy instance) in place of the
original if/elif chain.

Acknowledged the strategy_map as a genuine readability improvement over
the original chain, but identified a subtler problem: every time a new
payment type is added, the map itself needs to be updated too, meaning
extension of the system still requires modification somewhere, just moved
one level up rather than eliminated. Reasoned through where the map could
live to avoid this, and concluded there wasn't a clean home for it: placing
it in the abstract base class violates SRP (the base class shouldn't know
about every concrete subclass); placing it in PaymentProcessor violates
OCP (the same class needing modification for each new type, just relocated).
Proposed constructor injection instead: the calling code decides which
strategy to use and passes it in directly, with no central registry to
maintain at all:

```python
processor = PaymentProcessor(CreditCardPayment())
processor.process_payment(150.00)
```

Also replied to Joseph's post, which implemented Strategy through a
payment-processing scenario framed around African mobile money providers
(M-Pesa, MTN MoMo), with PaymentProcessor allowing an optional strategy at
construction (Optional[PaymentStrategy] = None) and a set_strategy()
method, guarded by a ValueError if process_payment() is called before a
strategy is set.

Noted the defensive ValueError guard as a solid pattern not used in my own
implementation, and specifically raised a design question: Joseph's
PaymentProcessor allows construction without a strategy (assigned later
via set_strategy()), whereas my own implementation requires a strategy at
instantiation (def __init__(self, strategy: PaymentStrategy)), making it
impossible for a PaymentProcessor to exist in an invalid state at all.

Joseph's response resolved this well: requiring a strategy at construction
is generally more robust, since it enforces a valid object state from the
start, but the optional/set_strategy() approach is genuinely preferable in
scenarios like dynamic UI workflows, where the processor object must exist
before the user has actually chosen a payment method. He proposed a
middle-ground: require an initial strategy in the constructor for safety,
while still exposing a setter for runtime flexibility, combining both
approaches rather than treating them as mutually exclusive.

## Reflection

By this point in the module, I was more able to see design patterns and
SOLID principles clearly. Deconstructing a system into its component
classes was starting to become second nature again, like an old muscle
that hadn't been used in years, suddenly back in shape.
