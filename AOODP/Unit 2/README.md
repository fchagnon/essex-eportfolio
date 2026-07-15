# Unit 2: Refactoring to SOLID Principles

Design a simple online shopping system (cart, total calculation, discounts),
starting from a poorly designed single-class implementation, then refactor it
to adhere to all five SOLID principles.

## Artefact

`solid_shopping_system.py` — refactored version of an original design where a
single `Order` class managed cart items, price calculation, *and* payment
processing via an if/elif chain on payment type.

**Resulting structure:**
- `PaymentMethod` (abstract base class) — defines a single-method contract, `pay(amount)`
- `CreditCardPayment`, `PaypalPayment`, `CryptoPayment` — each a standalone implementation of `PaymentMethod`
- `Order` — manages cart items and total calculation only; receives a `PaymentMethod` via constructor injection rather than creating one internally

## How Each SOLID Principle Was Applied

Worked through in the order that makes each one possible:

1. **SRP (Single Responsibility Principle)** — Payment processing was removed
   entirely from `Order`. `Order`'s only remaining job is managing the cart
   and calculating totals (including the discount rule, since pricing is an
   `Order` concern, not a payment concern).

2. **OCP (Open/Closed Principle)** — Each payment method lives in its own
   isolated class. `CryptoPayment` was written last, after everything else
   was "done," and required zero changes to any existing class — the system
   was open to that extension, closed to modifying what already worked.

3. **LSP (Liskov Substitution Principle)** — Every subclass provides a
   genuine, working `pay(amount)` implementation with the correct signature.
   None raises `NotImplementedError` or silently does nothing — any code
   holding a `PaymentMethod` can trust it will behave correctly, regardless
   of which concrete class it actually is.

4. **ISP (Interface Segregation Principle)** — `PaymentMethod` only promises
   one method: `pay()`. Methods like `refund()` or `split_payment()` were
   deliberately excluded, since not every conceivable payment method
   (cash, for instance) can honestly support them. The test applied: *if a
   child class would look at a method and say "this doesn't apply to me,"
   the interface is too broad.*

5. **DIP (Dependency Inversion Principle)** — `Order` depends only on the
   `PaymentMethod` abstraction, injected via its constructor, and never
   references `CreditCardPayment`, `PaypalPayment`, or `CryptoPayment` by
   name. The concrete choice is made by the calling code, outside `Order`
   entirely.

## Why This Order Specifically

SRP had to come first, since separating payment logic out of `Order` is what
creates the space for an abstraction to exist at all. DIP came last, since it
only makes sense once `PaymentMethod` exists as something to depend on. Each
principle in between builds on the one before it — OCP needs the separated
classes SRP created; LSP and ISP both shape what the abstraction from OCP is
allowed to promise.

## Proof Points in the Code

- `process_any_order()` accepts any `PaymentMethod` and never asks what type
  it actually is — SRP, LSP, and DIP all verified working together in a
  single function.
- The discount calculation living inside `Order.calculate_total()`, not in
  any payment class, is the concrete SRP boundary: pricing rules and payment
  processing are kept genuinely separate.
- `CryptoPayment`'s addition without touching any existing class is the OCP
  proof — extension without modification.

## Reflection

Working through this refactor made the five SOLID principles concrete rather
than abstract definitions to memorise — each one turned out to correspond to
a specific, nameable problem in the original design (one class doing three
jobs; an if/elif chain that would need editing for every new payment type;
the risk of a subclass being forced to fake-implement a method that didn't
apply to it). Mapping the refactoring steps to the principles myself, before
being told which was which, made the ordering click: SRP has to come first
because it creates the separation everything else depends on, and DIP has to
come last because it only makes sense once there's an abstraction to depend
on.
