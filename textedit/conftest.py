"""Open one empty TextEdit document per session, and close what each test opened."""

import pytest
from macuitest.lib.applescript_lib.applescript_wrapper import as_wrapper
from macuitest.lib.apps.application import Application
from macuitest.lib.core import wait_condition
from macuitest.lib.elements.controllers.keyboard_controller import keyboard
from macuitest.lib.elements.locators import standard_window_frame

from textedit.screens import Fonts
from textedit.screens import SaveSheet


def close_fonts_panel(app: Application) -> None:
    """Close the Fonts panel if it's open, since Command-T toggles it."""
    # activate() raises unless TextEdit comes to the front, so hotkeys can't land in another app.
    app.activate()
    # The panel joins the accessibility tree a moment after TextEdit activates.
    if Fonts.search.wait_displayed(timeout=1):
        keyboard.hotkey("command", "t")
        Fonts.search.wait_vanish()


@pytest.fixture(autouse=True, scope="session")
def textedit(permissions):
    """Launch TextEdit with an empty document of its own, and quit it when the session ends."""
    app = Application("TextEdit", location="/System/Applications")
    app.launch()
    # The tests never type into it, so it closes and quits without a save prompt.
    document = as_wrapper.tell_app("TextEdit", "get name of (make new document)")
    close_fonts_panel(app)
    if not wait_condition(lambda: standard_window_frame("TextEdit"), timeout=5):
        pytest.fail("TextEdit's document window didn't appear. See textedit/README.md.")
    yield app
    as_wrapper.tell_app("TextEdit", f'close document "{document}" saving no')
    app.quit()


@pytest.fixture
def save_sheet(textedit):
    """Open the Save sheet with Command-S, and cancel it if the test left it open."""
    textedit.activate()
    keyboard.hotkey("command", "s")
    if not SaveSheet.cancel.wait_displayed(timeout=3):
        pytest.fail("Command-S didn't open the Save sheet within 3 seconds")
    yield
    if SaveSheet.cancel.is_visible:
        SaveSheet.cancel.press()
        SaveSheet.cancel.wait_vanish()


@pytest.fixture
def fonts_panel(textedit):
    """Open the Fonts panel with Command-T, and close it if the test left it open."""
    textedit.activate()
    keyboard.hotkey("command", "t")
    if not Fonts.search.wait_displayed(timeout=3):
        pytest.fail("Command-T didn't open the Fonts panel within 3 seconds")
    yield
    close_fonts_panel(textedit)
