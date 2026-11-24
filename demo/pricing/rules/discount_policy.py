"""Discount rules."""
from pricing.data_types import CustomerTier
from pricing.rules._helpers.money import apply_basis_points
from pricing.rules.interface import DiscountRule


class DiscountPolicy(DiscountRule):
    """Decide the discount for an order subtotal.

    Not responsible for: tax, validation.
    """

    def discount(self, subtotal_pence: int, customer_tier: CustomerTier) -> int:
        """Return the discount for a subtotal.

        Args:
            subtotal_pence: Order subtotal in pence, at least 0.
            customer_tier: Customer tier. "vip" adds 5% on top of the base rate.

        Returns:
            Discount in pence, never more than the subtotal.

        Note:
            Base rate is 10% when the subtotal is GBP 100 or more, otherwise 0%.
        """
        rate_bps = 1_000 if subtotal_pence >= 10_000 else 0
        if customer_tier == "vip":
            rate_bps += 500
        return min(apply_basis_points(subtotal_pence, rate_bps), subtotal_pence)
