"""Drive Calculator by clicking screenshots of its keys, found with template matching."""

import pytest
from macuitest.lib.core import wait_condition
from macuitest.lib.elements.ui.monitor import monitor

from calculator.screens import Calculator
from calculator.screens import display_value

pytestmark = [
    pytest.mark.usefixtures("cleared"),
    # The key screenshots were captured on a 2x display.
    pytest.mark.skipif(not monitor.is_retina, reason="key screenshots need a 2x main display"),
]


def test_multiply_with_screenshots():
    keys = (
        Calculator.seven_image,
        Calculator.multiply_image,
        Calculator.six_image,
        Calculator.equals_image,
    )
    for key in keys:
        key.click_mouse()

    assert wait_condition(lambda: display_value() == "42", timeout=2), display_value()
