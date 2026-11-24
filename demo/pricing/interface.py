"""Public interface of the pricing component."""
from abc import ABC, abstractmethod

from pricing.data_types import Order, PriceBreakdown


class Pricer(ABC):
    """Price an order into subtotal, discount, tax and total.

    Not responsible for: reading orders, taking payment, formatting output.
    """

    @abstractmethod
    def price(self, order: Order) -> PriceBreakdown:
        """Price one order.

        Args:
            order: The order to price.

        Returns:
            Price breakdown in integer pence.

        Raises:
            ValueError: If the order is invalid, for example no items,
                a quantity below 1 or an unknown customer tier.

        Note:
            Does not modify ``order``.
        """
