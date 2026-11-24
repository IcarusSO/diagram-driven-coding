"""VAT calculation."""
from pricing.rules.interface import TaxRule

VAT_RATE_BPS = 2_000
BPS_DENOMINATOR = 10_000


class TaxCalculator(TaxRule):
    """Calculate VAT on a taxable amount.

    Not responsible for: discounts, validation.
    """

    def tax(self, taxable_pence: int) -> int:
        """Return the VAT on an amount.

        Args:
            taxable_pence: Amount to tax in pence, at least 0.

        Returns:
            VAT in pence at 20%, rounded half up.
        """
        whole_pence, remainder = divmod(taxable_pence * VAT_RATE_BPS, BPS_DENOMINATOR)
        return whole_pence + (1 if remainder * 2 >= BPS_DENOMINATOR else 0)
