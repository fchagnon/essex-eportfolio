from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Abstract Factory - payment provider families
# ---------------------------------------------------------------------------

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        """Attempt to charge amount. Return True on success."""
        ...


class RefundHandler(ABC):
    @abstractmethod
    def refund(self, amount: float) -> bool:
        """Attempt to refund amount. Return True on success."""
        ...


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        """Simulate a Stripe charge."""
        print(f"[Stripe] Successfully charged ${amount:.2f}")
        return True


class StripeRefundHandler(RefundHandler):
    def refund(self, amount: float) -> bool:
        """Simulate a Stripe refund."""
        print(f"[Stripe] Successfully refunded ${amount:.2f}")
        return True


class PayPalGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        """Simulate a PayPal charge."""
        print(f"[PayPal] Successfully charged ${amount:.2f} via Express Checkout")
        return True


class PayPalRefundHandler(RefundHandler):
    def refund(self, amount: float) -> bool:
        """Simulate a PayPal refund."""
        print(f"[PayPal] Successfully processed partner refund of ${amount:.2f}")
        return True


class PaymentProviderFactory(ABC):
    """
    Abstract Factory: each concrete factory produces a MATCHED pair -
    a gateway and a refund handler from the SAME provider.
    """

    @abstractmethod
    def create_gateway(self) -> PaymentGateway:
        ...

    @abstractmethod
    def create_refund_handler(self) -> RefundHandler:
        ...


class StripeProviderFactory(PaymentProviderFactory):
    def create_gateway(self) -> PaymentGateway:
        return StripeGateway()

    def create_refund_handler(self) -> RefundHandler:
        return StripeRefundHandler()


class PayPalProviderFactory(PaymentProviderFactory):
    def create_gateway(self) -> PaymentGateway:
        return PayPalGateway()

    def create_refund_handler(self) -> RefundHandler:
        return PayPalRefundHandler()
