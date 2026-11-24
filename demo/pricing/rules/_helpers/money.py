"""Private money helpers of the pricing component. Other folders must not import this."""


def apply_basis_points(amount_pence: int, basis_points: int) -> int:
    """Apply a rate to an amount using integer arithmetic.

    Args:
        amount_pence: Amount in pence, at least 0.
        basis_points: Rate in basis points. 10000 means 100%.

    Returns:
        The result in pence, rounded half up.
    """
    return (amount_pence * basis_points + 5_000) // 10_000
