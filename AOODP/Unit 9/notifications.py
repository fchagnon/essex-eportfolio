from abc import ABC, abstractmethod
from models import Order

# ---------------------------------------------------------------------------
# Observer pattern - order status notifications
# ---------------------------------------------------------------------------

class OrderObserver(ABC):
    """Interface for anything that wants to react to order events."""

    @abstractmethod
    def update(self, order, event: str):
        """
        Called by OrderProcessor when something happens to an order.
        event will be a string like "created", "shipped", "cancelled".
        """
        ...


class EmailNotifier(OrderObserver):
    def update(self, order, event: str):
        """
        Print (simulate) an email to order.user.email describing the event.
        No real email sending - this is a stand-in, same spirit as your
        Unit 11 EmailService example.
        """
        raise NotImplementedError


class SMSNotifier(OrderObserver):
    def update(self, order, event: str):
        """Same idea as EmailNotifier but simulate an SMS instead."""
        raise NotImplementedError
