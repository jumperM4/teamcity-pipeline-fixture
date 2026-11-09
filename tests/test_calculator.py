import pytest

from teamcity_fixture import add, divide


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 3, 5),
        (-4, -6, -10),
        (-7, 7, 0),
        (0, 0, 0),
    ],
)
def test_add(left: int, right: int, expected: int) -> None:
    assert add(left, right) == expected


@pytest.mark.parametrize(
    ("dividend", "divisor", "expected"),
    [
        (10.0, 2.0, 5.0),
        (-9.0, 3.0, -3.0),
        (0.0, 5.0, 0.0),
        (1.0, 4.0, 0.25),
    ],
)
def test_divide(dividend: float, divisor: float, expected: float) -> None:
    assert divide(dividend, divisor) == expected


def test_divide_rejects_zero_divisor() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        divide(5.0, 0.0)

