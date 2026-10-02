"""Check that every declared element resolves, without pressing anything.

Run this first after a macOS update.
"""

import pytest
from macuitest.lib.elements.locators.factories import AXLocator

from calculator.screens import Calculator
from calculator.screens import display_value

AX_ELEMENTS = [name for name, value in vars(Calculator).items() if isinstance(value, AXLocator)]


@pytest.mark.parametrize("name", AX_ELEMENTS)
def test_accessibility_elements_resolve(name):
    assert getattr(Calculator, name).item is not None


def test_calculator_is_in_basic_mode():
    assert "basic" in Calculator.mode.item.get_ax_attribute("AXIdentifier")


def test_the_display_reads_a_number():
    assert display_value().isdigit()
