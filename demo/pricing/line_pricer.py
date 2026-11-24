"""Line total calculation."""
from pricing.data_types import OrderItem


class LinePricer:
    """Calculate the subtotal of order lines.

    Not responsible for: discounts, tax.
    """

    def subtotal(self, items: list[OrderItem]) -> int:
        """Return the sum of unit price times quantity.

        Args:
            items: Order lines. Assumed to be valid.

        Returns:
            Subtotal in pence.
        """
        return sum(item["unit_price_pence"] * item["quantity"] for item in items)
