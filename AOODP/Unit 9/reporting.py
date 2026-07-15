from abc import ABC, abstractmethod
from models import Product, Order

# ---------------------------------------------------------------------------
# Visitor pattern - reporting/analytics separated from domain classes
# ---------------------------------------------------------------------------

class ReportVisitor(ABC):
    @abstractmethod
    def visit_product(self, product: Product):
        ...

    @abstractmethod
    def visit_order(self, order: Order):
        ...


class InventoryReportVisitor(ReportVisitor):
    """
    Accumulates stock-level data as it visits products.
    Doesn't need to touch orders meaningfully, but must implement
    visit_order() to satisfy the interface (can be a no-op).
    """

    def __init__(self):
        self.low_stock = []  # products below some threshold

    def visit_product(self, product: Product):
        """
        If product.stock is below a threshold (pick one, e.g. 10),
        append it to self.low_stock.
        """
        raise NotImplementedError

    def visit_order(self, order: Order):
        """No-op for this visitor - inventory doesn't care about orders."""
        raise NotImplementedError


class SalesReportVisitor(ReportVisitor):
    """
    Accumulates revenue data as it visits orders.
    """

    def __init__(self):
        self.total_revenue = 0.0
        self.orders_seen = 0

    def visit_product(self, product: Product):
        """No-op for this visitor - sales doesn't care about individual products."""
        raise NotImplementedError

    def visit_order(self, order: Order):
        """
        Add order.total() to self.total_revenue, increment self.orders_seen.
        """
        raise NotImplementedError
