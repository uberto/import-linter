import pytest

from importlinter.application import rendering


@pytest.mark.parametrize(
    "milliseconds, expected",
    [
        (0, "0ms"),
        (1, "1ms"),
        (532, "532ms"),
        (999, "999ms"),
        (1000, "1s"),
        (1234, "1.234s"),
        (2500, "2.5s"),
        (9999, "9.999s"),
        (10000, "10s"),
        (12400, "12s"),
    ],
)
def test_format_duration(milliseconds, expected):
    assert rendering._format_duration(milliseconds) == expected
