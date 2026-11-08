"""Example domain functions exercised by the fixture test suite."""


def add(left: int, right: int) -> int:
    """Return the sum of two integers."""
    return left + right


def divide(dividend: float, divisor: float) -> float:
    """Divide two numbers and reject an invalid zero divisor explicitly."""
    if divisor == 0:
        raise ValueError("divisor must not be zero")
    return dividend / divisor

