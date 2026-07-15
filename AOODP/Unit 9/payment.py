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
        """Simulate a Stripe charge (print + return True)."""
        raise NotImplementedError


class StripeRefundHandler(RefundHandler):
    def refund(self, amount: float) -> bool:
        raise NotImplementedError


class PayPalGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        raise NotImplementedError


class PayPalRefundHandler(RefundHandler):
    def refund(self, amount: float) -> bool:
        raise NotImplementedError


class PaymentProviderFactory(ABC):
    """
    Abstract Factory: each concrete factory produces a MATCHED pair -
    a gateway and a refund handler from the SAME provider. This is the
    bit that makes it Abstract Factory rather than a plain Factory Method:
    the two products must never be mixed (e.g. Stripe gateway + PayPal
    refund handler would be a bug this pattern prevents by construction).
    """

    @abstractmethod
    def create_gateway(self) -> PaymentGateway:
        ...

    @abstractmethod
    def create_refund_handler(self) -> RefundHandler:
        ...


class StripeProviderFactory(PaymentProviderFactory):
    def create_gateway(self) -> PaymentGateway:
        raise NotImplementedError

    def create_refund_handler(self) -> RefundHandler:
        raise NotImplementedError


class PayPalProviderFactory(PaymentProviderFactory):
    def create_gateway(self) -> PaymentGateway:
        raise NotImplementedError

    def create_refund_handler(self) -> RefundHandler:
        raise NotImplementedError
