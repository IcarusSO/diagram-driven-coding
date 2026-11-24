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
            # New rule: orders of GBP 200 or more get a 15% base discount instead of 10%
            ("standard", 19_999, 2_000),
            ("standard", 20_000, 3_000),
            ("vip", 20_000, 4_000),
        ]
        for tier, subtotal, expected in cases:
            with self.subTest(tier=tier, subtotal=subtotal):
                self.assertEqual(DiscountPolicy().discount(subtotal, tier), expected)
