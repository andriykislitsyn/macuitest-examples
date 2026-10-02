"""Mix element kinds the way a real suite does: each where it fits best."""

import pytest
from macuitest.lib.core import wait_condition
from macuitest.lib.elements.ui.monitor import monitor

from calculator.screens import Calculator
from calculator.screens import display_value

pytestmark = [
    pytest.mark.usefixtures("cleared"),
    # The multiply key is clicked by a screenshot captured on a 2x display.
    pytest.mark.skipif(not monitor.is_retina, reason="key screenshots need a 2x main display"),
]


def test_calculate_then_clear_with_mixed_element_kinds():
    Calculator.seven.press()
    Calculator.multiply_image.click_mouse()
    Calculator.six_as.click()
    Calculator.equals.press()
    assert wait_condition(lambda: display_value() == "42", timeout=2), display_value()

    Calculator.all_clear_text.click_mouse()

    assert wait_condition(lambda: display_value() == "0", timeout=2), display_value()
