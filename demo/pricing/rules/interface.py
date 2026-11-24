"""Public interfaces of the pricing rules sub-component."""
from abc import ABC, abstractmethod

from pricing.data_types import CustomerTier


class DiscountRule(ABC):
    """Decide the discount for an order subtotal.

    Not responsible for: tax, validation, order structure.
    """

    @abstractmethod
    def discount(self, subtotal_pence: int, customer_tier: CustomerTier) -> int:
        """Return the discount for a subtotal.

        Args:
            subtotal_pence: Order subtotal in pence, at least 0.
            customer_tier: Customer tier.

        Returns:
            Discount in pence, never more than the subtotal.
        """


class TaxRule(ABC):
    """Calculate tax on a taxable amount.

    Not responsible for: discounts, validation, order structure.
    """

    @abstractmethod
    def tax(self, taxable_pence: int) -> int:
        """Return the tax on an amount.

        Args:
            taxable_pence: Amount to tax in pence, at least 0.

        Returns:
            Tax in pence, rounded half up.
        """
