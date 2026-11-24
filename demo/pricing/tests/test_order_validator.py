import unittest
from typing import cast

from pricing import Order
from pricing.order_validator import OrderValidator


def valid_order() -> Order:
    return {"customer_tier": "standard", "items": [{"sku": "A", "unit_price_pence": 100, "quantity": 1}]}


class TestOrderValidator(unittest.TestCase):
    def test_accepts_a_valid_order(self) -> None:
        OrderValidator().validate(valid_order())

    def test_rejects_bad_orders(self) -> None:
        bad_changes: list[tuple[str, dict[str, object]]] = [
            ("unknown tier", {"customer_tier": "gold"}),
            ("no items", {"items": []}),
            ("zero quantity", {"items": [{"sku": "A", "unit_price_pence": 100, "quantity": 0}]}),
            ("negative price", {"items": [{"sku": "A", "unit_price_pence": -1, "quantity": 1}]}),
            ("empty sku", {"items": [{"sku": "", "unit_price_pence": 100, "quantity": 1}]}),
            ("float price", {"items": [{"sku": "A", "unit_price_pence": 1.5, "quantity": 1}]}),
        ]
        for name, change in bad_changes:
            with self.subTest(name):
                order = cast(Order, {**valid_order(), **change})  # invalid on purpose
                with self.assertRaises(ValueError):
                    OrderValidator().validate(order)
