import unittest

from pricing import CustomerTier
from pricing.rules.discount_policy import DiscountPolicy


class TestDiscountPolicy(unittest.TestCase):
    def test_discount_by_tier_and_subtotal(self) -> None:
        cases: list[tuple[CustomerTier, int, int]] = [
            ("standard", 9_999, 0),
            ("standard", 10_000, 1_000),
            ("vip", 5_000, 250),
            ("vip", 10_000, 1_500),
        ]
        for tier, subtotal, expected in cases:
            with self.subTest(tier=tier, subtotal=subtotal):
                self.assertEqual(DiscountPolicy().discount(subtotal, tier), expected)
