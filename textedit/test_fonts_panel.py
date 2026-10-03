"""Open TextEdit's Fonts panel, a floating window that a screen names with window=."""

import pytest
from macuitest.lib.apps.application import Finder
from macuitest.lib.elements.controllers.keyboard_controller import keyboard

from textedit.screens import Fonts
from textedit.screens import TextEdit

pytestmark = pytest.mark.usefixtures("fonts_panel")


def test_fonts_panel_controls_resolve_in_the_panel():
    controls = (Fonts.collections, Fonts.size, Fonts.search, Fonts.typography)

    assert all(control.wait_displayed() for control in controls)


def test_text_searches_only_the_screens_window():
    assert Fonts.helvetica.wait_displayed()
    assert TextEdit.untitled.wait_displayed()
    assert not Fonts.untitled.is_visible


def test_fonts_panel_leaves_accessibility_while_textedit_is_inactive(textedit):
    Finder().activate()
    assert Fonts.search.wait_vanish(timeout=3)

    textedit.activate()
    assert Fonts.search.wait_displayed(timeout=3)


def test_command_t_closes_the_panel():
    keyboard.hotkey("command", "t")

    assert Fonts.search.wait_vanish()
