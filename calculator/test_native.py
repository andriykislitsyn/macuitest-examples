"""Drive Calculator through accessibility elements: fast, and independent of how it looks."""

import pytest
from macuitest.lib.core import wait_condition

from calculator.screens import Calculator
from calculator.screens import display_value

pytestmark = pytest.mark.usefixtures("cleared")


def test_multiply_with_accessibility_elements():
    for key in (Calculator.seven, Calculator.multiply, Calculator.six, Calculator.equals):
        key.press()

    assert wait_condition(lambda: display_value() == "42", timeout=2), display_value()
