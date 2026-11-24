import unittest

from pricing.rules.tax_calculator import TaxCalculator


class TestTaxCalculator(unittest.TestCase):
    def test_vat_is_20_percent_rounded_half_up(self) -> None:
        cases = [(0, 0), (1, 0), (2, 0), (3, 1), (4, 1), (1_999, 400), (10_000, 2_000), (12_345, 2_469)]
        for taxable, expected in cases:
            with self.subTest(taxable=taxable):
                self.assertEqual(TaxCalculator().tax(taxable), expected)
