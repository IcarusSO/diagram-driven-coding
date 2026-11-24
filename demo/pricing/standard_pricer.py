"""Standard pricing implementation."""
from pricing.data_types import Order, PriceBreakdown
from pricing.interface import Pricer
from pricing.line_pricer import LinePricer
from pricing.order_validator import OrderValidator
from pricing.rules import DiscountRule, TaxRule


class StandardPricer(Pricer):
    """Price an order by validating it, then applying line prices, discount and tax in turn.

    Not responsible for: any calculation rule itself.
    """

    def __init__(self, discount_rule: DiscountRule, tax_rule: TaxRule) -> None:
        """Create a pricer.

        Args:
            discount_rule: Rule that decides the discount.
            tax_rule: Rule that calculates the tax.
        """
        self._validator = OrderValidator()
        self._line_pricer = LinePricer()
        self._discount_rule = discount_rule
        self._tax_rule = tax_rule

    def price(self, order: Order) -> PriceBreakdown:
        """Price one order.

        Args:
            order: The order to price.

        Returns:
            Price breakdown in integer pence.

        Raises:
            ValueError: If the order is invalid.
        """
        self._validator.validate(order)
        subtotal_pence = self._line_pricer.subtotal(order["items"])
        discount_pence = self._discount_rule.discount(subtotal_pence, order["customer_tier"])
        tax_pence = self._tax_rule.tax(subtotal_pence - discount_pence)
        return {
            "subtotal_pence": subtotal_pence,
            "discount_pence": discount_pence,
            "tax_pence": tax_pence,
            "total_pence": subtotal_pence - discount_pence + tax_pence,
        }
