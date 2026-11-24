"""VAT calculation."""
from pricing.rules.interface import TaxRule


class TaxCalculator(TaxRule):
    """Calculate VAT on a taxable amount.

    Not responsible for: discounts, validation.
    """

    def tax(self, taxable_pence: int) -> int:
        """Return the VAT on an amount."""
        return int(taxable_pence * 0.2)
