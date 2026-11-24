"""Text receipts."""
from pricing import Order, default_pricer


def _gbp(pence: int) -> str:
    """Format pence as pounds, for example 1999 becomes "£19.99"."""
    return f"£{pence / 100:.2f}"


def render_receipt(order: Order) -> str:
    """Render an order as a plain-text receipt.

    Args:
        order: The order to price and print.

    Returns:
        Four lines: subtotal, discount, VAT and total, in pounds.

    Raises:
        ValueError: If the order is invalid.
    """
    result = default_pricer().price(order)
    return "\n".join([
        f"Subtotal: {_gbp(result['subtotal_pence'])}",
        f"Discount: {_gbp(result['discount_pence'])}",
        f"VAT: {_gbp(result['tax_pence'])}",
        f"Total: {_gbp(result['total_pence'])}",
    ])
