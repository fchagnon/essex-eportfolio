from models import User, Product, Order
from notifications import OrderObserver
from payment import PaymentProviderFactory
from reporting import ReportVisitor, SalesReportVisitor
from repositories import ProductRepository, OrderRepository

# ---------------------------------------------------------------------------
# Business Logic Layer
# ---------------------------------------------------------------------------

class UserManager:
    def __init__(self, users: dict = None):
        self.users = users or {}

    def register(self, user: User):
        """Store the user keyed by user_id. Raise ValueError if id exists."""
        raise NotImplementedError

    def get(self, user_id):
        """Return the User or None."""
        raise NotImplementedError


class ProductCatalog:
    def __init__(self, repository: ProductRepository):
        """
        DI: repository is injected, not constructed here. This is what
        makes ProductCatalog testable in isolation with a fake repository,
        same principle as your Unit 11 UserManager/NotificationService work.
        """
        self.repository = repository

    def add_product(self, product: Product):
        raise NotImplementedError

    def find(self, product_id):
        raise NotImplementedError

    def generate_report(self, visitor: ReportVisitor):
        """
        Iterate over all products in the repository and call
        product.accept(visitor) on each. This is the mechanism that
        drives the Visitor pattern.
        """
        raise NotImplementedError


class OrderProcessor:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_factory: PaymentProviderFactory,
        observers: list = None,
    ):
        """
        DI: both the repository and the payment factory are injected.
        Notice OrderProcessor never instantiates StripeGateway or
        PayPalGateway directly - it only ever talks to the abstract
        PaymentGateway/RefundHandler interfaces, obtained via whichever
        factory was passed in. This is the point of Abstract Factory:
        swapping payment providers means passing a different factory,
        zero changes to OrderProcessor itself.
        """
        self.order_repository = order_repository
        self.payment_factory = payment_factory
        self.observers = observers or []

    def add_observer(self, observer: OrderObserver):
        raise NotImplementedError

    def _notify(self, order: Order, event: str):
        """Call update(order, event) on every registered observer."""
        raise NotImplementedError

    def place_order(self, order: Order) -> bool:
        """
        1. Get a PaymentGateway from self.payment_factory and charge
           order.total().
        2. If charge succeeds: save the order via self.order_repository,
           notify observers with event="created", return True.
        3. If charge fails: notify observers with event="payment_failed",
           return False.
        """
        raise NotImplementedError

    def cancel_order(self, order_id) -> bool:
        """
        1. Look up the order via self.order_repository.
        2. If found, get a RefundHandler from self.payment_factory and
           refund order.total().
        3. Notify observers with event="cancelled".
        4. Return True/False based on whether the order was found.
        """
        raise NotImplementedError

    def generate_sales_report(self, visitor: SalesReportVisitor):
        """
        Iterate over all orders in the repository and call
        order.accept(visitor) on each.
        """
        raise NotImplementedError
