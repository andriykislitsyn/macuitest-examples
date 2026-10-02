"""Launch Calculator once per session and start every input test from a cleared display."""

import pytest
from macuitest.lib.apps.application import Application
from macuitest.lib.core import wait_condition
from macuitest.lib.elements.locators.accessibility import standard_window_frame

from calculator.screens import Calculator
from calculator.screens import display_value


@pytest.fixture(autouse=True, scope="session")
def calculator(permissions):
    app = Application("Calculator", location="/System/Applications")
    app.launch()
    app.activate()
    # Calculator reports no accessibility window until it's active, and briefly after.
    if not wait_condition(lambda: standard_window_frame("Calculator"), timeout=5):
        pytest.fail("Calculator's window didn't appear within 5 seconds")
    if "basic" not in Calculator.mode.item.get_ax_attribute("AXIdentifier"):
        pytest.skip("Switch Calculator to Basic mode (View > Basic), then run again")
    yield app
    app.quit()


@pytest.fixture
def cleared():
    Calculator.all_clear.press()
    assert wait_condition(lambda: display_value() == "0", timeout=2), display_value()
