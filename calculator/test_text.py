"""Type into Calculator and read the result with Apple Vision."""

import pytest
from macuitest.lib.elements.controllers.keyboard_controller import keyboard
from macuitest.lib.elements.visible_text import VisibleText

from calculator.screens import Calculator

pytestmark = pytest.mark.usefixtures("cleared")


def test_multiply_by_typing_and_read_the_result_on_screen():
    keyboard.write("7*6=")

    # Vision can't read the single-character keys, but it reads a two-digit result.
    assert VisibleText("42").wait_displayed(region=Calculator.display.region(margin=8))
