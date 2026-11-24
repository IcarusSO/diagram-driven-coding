"""VAT calculation."""
from pricing.rules._helpers.money import apply_basis_points
from pricing.rules.interface import TaxRule

VAT_RATE_BPS = 2_000


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
        return apply_basis_points(taxable_pence, VAT_RATE_BPS)
