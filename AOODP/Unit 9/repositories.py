from abc import ABC, abstractmethod
from models import Product, Order

# ---------------------------------------------------------------------------
# Data Access Layer - Repository/DAO pattern
# ---------------------------------------------------------------------------

class ProductRepository(ABC):
    """Interface. Swappable for a real DB-backed implementation later."""

    @abstractmethod
    def get(self, product_id):
        ...

    @abstractmethod
    def save(self, product):
        ...

    @abstractmethod
    def all(self):
        ...


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._products = {}

    def get(self, product_id):
        """Return the Product with this id, or None if not found."""
        raise NotImplementedError

    def save(self, product):
        """Store/overwrite the product keyed by its product_id."""
        raise NotImplementedError

    def all(self):
        """Return a list of all stored products."""
        raise NotImplementedError


class OrderRepository(ABC):
    @abstractmethod
    def get(self, order_id):
        ...

    @abstractmethod
    def save(self, order):
        ...

    @abstractmethod
    def all(self):
        ...


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders = {}

    def get(self, order_id):
        raise NotImplementedError

    def save(self, order):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError
