"""Daily sales report."""
from pricing import Order, default_pricer


def render_daily_sales(orders: list[Order]) -> str:
    """Summarise one day of orders.

    Args:
        orders: All orders of the day.

    Returns:
        Two lines: the number of orders and the sales total in pounds.

    Raises:
        ValueError: If any order is invalid.
    """
    pricer = default_pricer()
    total_pence = sum(pricer.price(order)["total_pence"] for order in orders)
    return f"Orders: {len(orders)}\nSales: £{total_pence / 100:.2f}"
