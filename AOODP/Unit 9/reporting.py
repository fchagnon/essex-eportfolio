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
    def __init__(self, threshold: int = 10) -> None:
        self.threshold = threshold
        self.low_stock: list[Product] = []

    def visit_product(self, product: Product) -> None:
        if product.stock < self.threshold:
            self.low_stock.append(product)

    def visit_order(self, order: Order) -> None:
        pass

class SalesReportVisitor(ReportVisitor):
    """
    Accumulates revenue data as it visits orders.
    """
    def __init__(self) -> None:
        self.total_revenue: float = 0.0
        self.orders_seen: int = 0

    def visit_product(self, product: Product) -> None:
        pass

    def visit_order(self, order: Order) -> None:
        self.total_revenue += order.total()
        self.orders_seen += 1
