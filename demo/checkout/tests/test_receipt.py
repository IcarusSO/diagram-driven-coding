import unittest

from checkout.receipt import render_receipt
from pricing import Order


class TestReceipt(unittest.TestCase):
    def test_receipt_shows_each_amount_in_pounds(self) -> None:
        order: Order = {"customer_tier": "standard", "items": [{"sku": "A", "unit_price_pence": 1999, "quantity": 1}]}
        self.assertEqual(
            render_receipt(order),
            "Subtotal: £19.99\nDiscount: £0.00\nVAT: £4.00\nTotal: £23.99",
        )
