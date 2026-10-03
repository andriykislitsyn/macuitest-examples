"""Mix element kinds the way a real suite does: each where it fits best."""

import pytest
from macuitest.lib.core import wait_condition

from calculator.screens import Calculator
from calculator.screens import display_value

pytestmark = pytest.mark.usefixtures("cleared")


def test_calculate_then_clear_with_mixed_element_kinds():
    Calculator.seven.press()
    Calculator.multiply_image.click_mouse()
    Calculator.six_as.click()
    Calculator.equals.press()
    assert wait_condition(lambda: display_value() == "42", timeout=2), display_value()

    Calculator.all_clear_text.click_mouse()

    assert wait_condition(lambda: display_value() == "0", timeout=2), display_value()
