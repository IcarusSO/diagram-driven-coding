"""Validation of incoming orders."""
from typing import get_args

from pricing.data_types import CustomerTier, Order

VALID_TIERS = get_args(CustomerTier)


class OrderValidator:
    """Check that an order has a valid shape and valid values.

    Not responsible for: pricing.
    """

    def validate(self, order: Order) -> None:
        """Check an order at runtime, because callers may pass untrusted data.

        Args:
            order: The order to check.

        Raises:
            ValueError: If the customer tier is unknown, there are no items,
                an item has an empty sku, a negative or non-integer price,
                or a quantity below 1.
        """
        if order.get("customer_tier") not in VALID_TIERS:
            raise ValueError("unknown customer_tier")
        items = order.get("items")
        if not items:
            raise ValueError("order has no items")
        for item in items:
            if not isinstance(item.get("sku"), str) or not item["sku"]:
                raise ValueError("item needs a non-empty sku")
            unit_price = item.get("unit_price_pence")
            if isinstance(unit_price, bool) or not isinstance(unit_price, int) or unit_price < 0:
                raise ValueError("unit_price_pence must be a non-negative integer")
            quantity = item.get("quantity")
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
                raise ValueError("quantity must be an integer of at least 1")
