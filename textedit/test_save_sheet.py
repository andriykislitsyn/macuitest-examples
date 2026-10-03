"""Open TextEdit's Save sheet, check its controls, and cancel without saving."""

import pytest

from textedit.screens import SaveSheet
from textedit.screens import front_window_name

pytestmark = pytest.mark.usefixtures("save_sheet")


def test_save_sheet_suggests_the_document_name():
    assert SaveSheet.name_field.value == front_window_name()


def test_text_finds_a_sheet_label_in_the_document_window():
    assert SaveSheet.save_as_label.wait_displayed()


def test_cancel_closes_the_sheet_without_saving():
    name = front_window_name()

    SaveSheet.cancel.press()

    assert SaveSheet.cancel.wait_vanish()
    assert front_window_name() == name


def test_a_closed_sheets_button_raises_when_pressed():
    SaveSheet.cancel.press()
    assert SaveSheet.cancel.wait_vanish()

    with pytest.raises(LookupError, match="SaveSheet.cancel"):
        SaveSheet.cancel.press()


def test_applescript_cancel_closes_the_sheet():
    SaveSheet.cancel_as.click()

    assert SaveSheet.cancel_as.wait_vanish()
