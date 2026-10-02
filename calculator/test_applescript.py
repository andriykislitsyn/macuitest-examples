"""Drive Calculator through AppleScript locators, resolved by System Events."""

import pytest
from macuitest.lib.core import wait_condition

from calculator.screens import Calculator
from calculator.screens import display_value

pytestmark = pytest.mark.usefixtures("cleared")


def test_multiply_with_applescript_elements():
    keys = (Calculator.seven_as, Calculator.multiply_as, Calculator.six_as, Calculator.equals_as)
    for key in keys:
        key.click()

    assert wait_condition(lambda: display_value() == "42", timeout=2), display_value()
