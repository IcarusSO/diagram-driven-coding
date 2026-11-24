"""Behavioural contract of Pricer.

Discount amounts are deliberately not hard-coded here: discount rules are
tested by DiscountPolicy's own tests, so changing a rule does not touch this file.
"""
import copy
import unittest
from typing import cast

from pricing import CustomerTier, Order, default_pricer


def make_order(tier: str, *items: tuple[str, int, int]) -> Order:
    return {
        "customer_tier": cast(CustomerTier, tier),  # tests may pass invalid tiers on purpose
        "items": [{"sku": sku, "unit_price_pence": price, "quantity": qty} for sku, price, qty in items],
    }


class TestPricerContract(unittest.TestCase):
    def setUp(self) -> None:
        self.pricer = default_pricer()

    def test_small_order_breakdown_in_pence(self) -> None:
        result = self.pricer.price(make_order("standard", ("A", 1999, 1)))
        self.assertEqual(result, {
            "subtotal_pence": 1999, "discount_pence": 0, "tax_pence": 400, "total_pence": 2399,
        })

    def test_quantity_multiplies_unit_price(self) -> None:
        result = self.pricer.price(make_order("standard", ("A", 500, 2)))
        self.assertEqual(result["subtotal_pence"], 1000)
        self.assertEqual(result["total_pence"], 1200)

    def test_breakdown_always_adds_up(self) -> None:
        orders = [
            make_order("standard", ("A", 1999, 1)),
            make_order("standard", ("A", 5000, 5)),
            make_order("vip", ("A", 12000, 1)),
            make_order("vip", ("A", 300, 3), ("B", 99, 2)),
        ]
        for order in orders:
            with self.subTest(order=order):
                result = self.pricer.price(order)
                self.assertTrue(all(isinstance(value, int) for value in result.values()))
                self.assertGreaterEqual(result["discount_pence"], 0)
                self.assertLessEqual(result["discount_pence"], result["subtotal_pence"])
                self.assertEqual(
                    result["total_pence"],
                    result["subtotal_pence"] - result["discount_pence"] + result["tax_pence"],
                )

    def test_result_has_the_fields_downstream_code_depends_on(self) -> None:
        result = self.pricer.price(make_order("standard", ("A", 100, 1)))
        self.assertEqual(
            set(result), {"subtotal_pence", "discount_pence", "tax_pence", "total_pence"}
        )

    def test_invalid_orders_raise_value_error(self) -> None:
        invalid_orders: list[Order] = [
            {"customer_tier": "standard", "items": []},
            make_order("gold", ("A", 100, 1)),
            make_order("standard", ("A", 100, 0)),
        ]
        for order in invalid_orders:
            with self.subTest(order=order):
                with self.assertRaises(ValueError):
                    self.pricer.price(order)

    def test_does_not_mutate_the_order(self) -> None:
        order = make_order("vip", ("A", 12000, 1))
        before = copy.deepcopy(order)
        self.pricer.price(order)
        self.assertEqual(order, before)
