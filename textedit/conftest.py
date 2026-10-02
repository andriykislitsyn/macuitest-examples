"""Open one empty TextEdit document per session, and close what each test opened."""

import pytest
from macuitest.lib.applescript_lib.applescript_wrapper import as_wrapper
from macuitest.lib.apps.application import Application
from macuitest.lib.core import wait_condition
from macuitest.lib.elements.controllers.keyboard_controller import keyboard
from macuitest.lib.elements.locators import standard_window_frame

from textedit.screens import SaveSheet


def bring_to_front(app: Application) -> None:
    """Activate `app` and wait until it's frontmost, so hotkeys can't land in another app."""
    app.activate()
    if not wait_condition(lambda: app.is_frontmost, timeout=3):
        pytest.fail("TextEdit didn't come to the front within 3 seconds")


@pytest.fixture(autouse=True, scope="session")
def textedit(permissions):
    """Launch TextEdit with an empty document of its own, and quit it when the session ends."""
    app = Application("TextEdit", location="/System/Applications")
    app.launch()
    # The tests never type into it, so it closes and quits without a save prompt.
    document = as_wrapper.tell_app("TextEdit", "get name of (make new document)")
    bring_to_front(app)
    if not wait_condition(lambda: standard_window_frame("TextEdit"), timeout=5):
        pytest.fail("TextEdit's document window didn't appear. See textedit/README.md.")
    yield app
    as_wrapper.tell_app("TextEdit", f'close document "{document}" saving no')
    app.quit()


@pytest.fixture
def save_sheet(textedit):
    """Open the Save sheet with Command-S, and cancel it if the test left it open."""
    bring_to_front(textedit)
    keyboard.hotkey("command", "s")
    if not wait_condition(lambda: SaveSheet.cancel.is_visible, timeout=3):
        pytest.fail("Command-S didn't open the Save sheet within 3 seconds")
    yield
    if SaveSheet.cancel.is_visible:
        SaveSheet.cancel.press()
        SaveSheet.cancel.wait_vanish()
