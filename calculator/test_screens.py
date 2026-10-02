"""Check that every declared element resolves, without pressing anything.

Run this first after a macOS update.
"""

import pytest
from macuitest.lib.elements.locators.factories import AppleScriptLocator
from macuitest.lib.elements.locators.factories import AXLocator
from macuitest.lib.elements.locators.factories import ImageLocator
from macuitest.lib.elements.ui.monitor import monitor

from calculator.screens import Calculator
from calculator.screens import display_value


def declared(kind):
    return [name for name, value in vars(Calculator).items() if isinstance(value, kind)]


@pytest.mark.parametrize("name", declared(AXLocator))
def test_accessibility_elements_resolve(name):
    assert getattr(Calculator, name).item is not None


@pytest.mark.parametrize("name", declared(AppleScriptLocator))
def test_applescript_elements_exist(name):
    assert getattr(Calculator, name).is_visible


@pytest.mark.skipif(not monitor.is_retina, reason="key screenshots need a 2x main display")
@pytest.mark.parametrize("name", declared(ImageLocator))
def test_screenshots_match_on_screen(name):
    assert getattr(Calculator, name).wait_displayed()


def test_visible_labels_read_on_screen():
    # `result` is left out: it only appears after a calculation.
    assert Calculator.all_clear_text.wait_displayed()


def test_calculator_is_in_basic_mode():
    assert "basic" in (Calculator.mode.item.get_ax_attribute("AXIdentifier") or "")


def test_the_display_shows_a_value():
    assert display_value()
