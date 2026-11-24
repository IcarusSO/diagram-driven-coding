import unittest

from pricing import Order
from reports.daily_sales import render_daily_sales


class TestDailySales(unittest.TestCase):
    def test_sums_order_totals(self) -> None:
        orders: list[Order] = [
            {"customer_tier": "standard", "items": [{"sku": "A", "unit_price_pence": 1999, "quantity": 1}]},
            {"customer_tier": "standard", "items": [{"sku": "B", "unit_price_pence": 500, "quantity": 2}]},
        ]
        self.assertEqual(render_daily_sales(orders), "Orders: 2\nSales: £35.99")

    def test_no_orders(self) -> None:
        self.assertEqual(render_daily_sales([]), "Orders: 0\nSales: £0.00")
