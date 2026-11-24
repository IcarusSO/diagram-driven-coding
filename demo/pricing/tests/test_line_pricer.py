import unittest

from pricing import OrderItem
from pricing.line_pricer import LinePricer


class TestLinePricer(unittest.TestCase):
    def test_sums_price_times_quantity(self) -> None:
        items: list[OrderItem] = [
            {"sku": "A", "unit_price_pence": 250, "quantity": 2},
            {"sku": "B", "unit_price_pence": 99, "quantity": 3},
        ]
        self.assertEqual(LinePricer().subtotal(items), 797)
