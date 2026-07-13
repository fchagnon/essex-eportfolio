# =============================================================================
# SOLID Principles: Refactored Online Shopping System
# =============================================================================
# This file demonstrates all five SOLID principles applied to a simple
# online shopping system with cart management and payment processing.
#
# The original (poorly designed) code had a single Order class that:
#   - Managed cart items
#   - Calculated totals
#   - Processed payments via an if/elif chain
#
# All three responsibilities in one class = SRP, OCP, and DIP violations.
# The refactored code below addresses each violation step by step.
# =============================================================================

from abc import ABC, abstractmethod


# =============================================================================
# STEP 1: PaymentMethod Abstract Class
# --- Addresses: SRP, OCP, LSP, ISP, DIP ---
#
# SRP: Payment processing logic is completely removed from Order.
#      PaymentMethod's only responsibility is defining the payment contract.
#
# OCP: New payment methods are added as NEW classes, never by modifying
#      this abstract class or any existing payment class.
#
# ISP: Only ONE abstract method lives here — pay(amount).
#      Every conceivable payment method (credit, crypto, cash, PayPal)
#      can genuinely honor this promise. No method is included that would
#      force a child class into a meaningless or dishonest implementation.
#
# DIP: This abstraction is the layer that Order will depend on —
#      not any specific concrete payment class below.
# =============================================================================

class PaymentMethod(ABC):

    @abstractmethod
    def pay(self, amount):
        """
        Contract: every child class MUST implement pay(amount).
        The contract is intentionally narrow — just pay().
        Methods like refund() or split_payment() are excluded because
        not every conceivable payment method supports them (ISP).
        Forcing children to implement inapplicable methods would lead
        to dishonest implementations and LSP violations.
        """
        pass


# =============================================================================
# STEP 2 & 3: Concrete Payment Classes
# --- Addresses: OCP, LSP ---
#
# OCP: Each payment method lives in its own isolated class.
#      Adding CryptoPayment years later requires ZERO changes to
#      CreditCardPayment, PaypalPayment, or any other existing class.
#      The system is extended, never modified.
#
# LSP: Every subclass implements pay(amount) with the correct signature
#      and a genuine, working implementation. Any code that accepts a
#      PaymentMethod can receive ANY of these subclasses and trust that
#      pay() will work as expected — no surprises, no crashes.
#      No subclass raises NotImplementedError or silently does nothing.
# =============================================================================

class CreditCardPayment(PaymentMethod):

    def pay(self, amount):
        """
        Fulfills the PaymentMethod contract for credit card processing.
        Same signature as the abstract method — LSP honored.
        """
        print(f"  Processing credit card payment of ${amount:.2f}...")


class PaypalPayment(PaymentMethod):

    def pay(self, amount):
        """
        Fulfills the PaymentMethod contract for PayPal processing.
        Completely isolated from CreditCardPayment — OCP honored.
        A bug introduced here cannot affect any other payment class.
        """
        print(f"  Processing PayPal payment of ${amount:.2f}...")


class CryptoPayment(PaymentMethod):
    """
    Added years later — without touching a single line of existing code.
    This is OCP in practice: the system was open for this extension,
    and closed to modification of what already worked.

    LSP: CryptoPayment can replace PaymentMethod anywhere in the codebase.
    It honors the contract — pay(amount) is implemented, genuine, and works.
    """

    def pay(self, amount):
        print(f"  Processing crypto payment of ${amount:.2f}...")


# =============================================================================
# STEP 4 & 5: Order Class
# --- Addresses: SRP, DIP ---
#
# SRP: Order has exactly ONE responsibility — managing the cart and
#      calculating the total. It has no knowledge of HOW payments are
#      processed. Its only reason to change is if cart or pricing logic changes.
#
# DIP: Order depends on the PaymentMethod ABSTRACTION, injected via __init__.
#      It never references CreditCardPayment, PaypalPayment, or CryptoPayment
#      by name. It only knows "I have something that can call .pay(amount)."
#      This is Dependency Injection — the concrete payment class is chosen
#      OUTSIDE of Order and passed in, keeping Order blissfully unaware.
# =============================================================================

class Order:

    def __init__(self, payment_method: PaymentMethod):
        """
        DIP: PaymentMethod (the abstraction) is injected from outside.
        Order never decides which payment class to use — that decision
        belongs to the calling code. Order just trusts the contract.
        """
        self.items = []
        self.payment_method = payment_method  # Abstraction, not a concrete class

    def add_item(self, item):
        """
        SRP: Managing cart items is one of Order's two legitimate concerns.
        """
        self.items.append(item)
        print(f"  Added '{item.name}' (${item.price:.2f}) to cart.")

    def calculate_total(self):
        """
        SRP: Calculating the order total is Order's other legitimate concern.
        Applies a discount if the total exceeds $100 — pricing logic
        belongs here, not in any payment class.
        """
        subtotal = sum(item.price for item in self.items)

        # Discount logic lives here — a pricing rule is an Order concern,
        # not a payment concern (SRP)
        discount = 0.10 if subtotal > 100 else 0.0
        total = subtotal * (1 - discount)

        if discount:
            print(f"  Subtotal: ${subtotal:.2f} | Discount: {int(discount*100)}% "
                  f"| Total: ${total:.2f}")
        else:
            print(f"  Total: ${total:.2f}")

        return total

    def checkout(self):
        """
        Ties the two Order responsibilities together, then delegates
        payment to whatever PaymentMethod was injected.

        DIP in action: self.payment_method.pay(total) works identically
        whether the injected class is CreditCardPayment, PaypalPayment,
        CryptoPayment, or any future payment class yet to be written.
        Order doesn't know or care which one it is.
        """
        print("  Calculating order total...")
        total = self.calculate_total()
        self.payment_method.pay(total)  # Delegates to the abstraction
        print("  Order complete.\n")


# =============================================================================
# Simple Product class — a lightweight data container
# Not the focus of SOLID here, but needed to give Order something to manage.
# =============================================================================

class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price


# =============================================================================
# --- Demo / Test ---
# =============================================================================

print("=" * 55)
print("Order 1: Credit Card — small order, no discount")
print("=" * 55)
# DIP: CreditCardPayment is chosen HERE, outside of Order.
# Order never sees this class name — only receives the abstraction.
order1 = Order(payment_method=CreditCardPayment())
order1.add_item(Product("Keyboard", 45.00))
order1.add_item(Product("Mouse", 30.00))
order1.checkout()

print("=" * 55)
print("Order 2: PayPal — large order, 10% discount applied")
print("=" * 55)
# OCP: Swapping to PaypalPayment required zero changes to Order,
# CreditCardPayment, or any other existing class.
order2 = Order(payment_method=PaypalPayment())
order2.add_item(Product("Monitor", 299.99))
order2.add_item(Product("HDMI Cable", 15.00))
order2.checkout()

print("=" * 55)
print("Order 3: Crypto — added later, zero existing code modified")
print("=" * 55)
# OCP + LSP: CryptoPayment was added as a pure extension.
# It slots in as a PaymentMethod replacement without any issues —
# same contract, same behavior from Order's perspective.
order3 = Order(payment_method=CryptoPayment())
order3.add_item(Product("Laptop", 899.00))
order3.add_item(Product("Laptop Bag", 49.99))
order3.checkout()

print("=" * 55)
print("LSP Proof: All payment methods are interchangeable")
print("=" * 55)
# LSP: This function accepts any PaymentMethod child.
# It has no idea which concrete class it receives — nor should it.
# All three work identically from this function's perspective.
def process_any_order(payment_method: PaymentMethod):
    order = Order(payment_method)
    order.add_item(Product("Test Product", 50.00))
    order.checkout()

for method in [CreditCardPayment(), PaypalPayment(), CryptoPayment()]:
    print(f"  Testing with {type(method).__name__}:")
    process_any_order(method)
