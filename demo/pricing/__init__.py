"""Pricing component. Other folders may use only what is exported here."""
from pricing.data_types import CustomerTier, Order, OrderItem, PriceBreakdown
from pricing.interface import Pricer
from pricing.rules import default_discount_rule, default_tax_rule
from pricing.standard_pricer import StandardPricer

__all__ = ["CustomerTier", "Order", "OrderItem", "PriceBreakdown", "Pricer", "default_pricer"]


def default_pricer() -> Pricer:
    """Return the pricer implementation currently in use.

    This is where the implementation and its dependencies are wired together.

    Returns:
        A ready-to-use Pricer.
    """
    return StandardPricer(default_discount_rule(), default_tax_rule())
