"""Pricing rules sub-component. The pricing component may use only what is exported here."""
from pricing.rules.discount_policy import DiscountPolicy
from pricing.rules.interface import DiscountRule, TaxRule
from pricing.rules.tax_calculator import TaxCalculator

__all__ = ["DiscountRule", "TaxRule", "default_discount_rule", "default_tax_rule"]


def default_discount_rule() -> DiscountRule:
    """Return the discount rule currently in use.

    Returns:
        A ready-to-use DiscountRule.
    """
    return DiscountPolicy()


def default_tax_rule() -> TaxRule:
    """Return the tax rule currently in use.

    Returns:
        A ready-to-use TaxRule.
    """
    return TaxCalculator()
