"""Public data types of the pricing component."""
from typing import Literal, TypedDict

CustomerTier = Literal["standard", "vip"]


class OrderItem(TypedDict):
    """One line of an order.

    Attributes:
        sku: Product identifier, non-empty.
        unit_price_pence: Price of one unit in pence, at least 0.
        quantity: Number of units, at least 1.
    """

    sku: str
    unit_price_pence: int
    quantity: int


class Order(TypedDict):
    """An order to be priced.

    Attributes:
        customer_tier: Customer tier. Decides which discounts apply.
        items: Order lines. At least one.
    """

    customer_tier: CustomerTier
    items: list[OrderItem]


class PriceBreakdown(TypedDict):
    """Price details of an order. All amounts are integer pence.

    Attributes:
        subtotal_pence: Sum of unit price times quantity over all items.
        discount_pence: Discount applied. Never more than the subtotal.
        tax_pence: VAT charged on the subtotal minus the discount.
        total_pence: subtotal_pence - discount_pence + tax_pence.
    """

    subtotal_pence: int
    discount_pence: int
    tax_pence: int
    total_pence: int
