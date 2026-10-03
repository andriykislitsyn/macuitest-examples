# TextEdit examples

This suite shows the two window cases that Calculator doesn't have: a sheet inside a document window, and a floating panel that a screen names with `window=`. It opens TextEdit's Save sheet and Fonts panel, checks their controls, and closes them. It never types into a document or saves one.

## Requirements

The suite expects the following setup:

- macOS 26. TextEdit's accessibility tree can change with any macOS release.
- New documents in rich text with the default font, Helvetica. Check both in **TextEdit > Settings > New Document**. `Fonts.helvetica` reads the font name in the Fonts panel.
- No Open panel when TextEdit starts. TextEdit shows one when its iCloud Drive is on, and the suite isn't tested with it. If it appears, close it before you run the suite.

## Run the suite

Run the whole suite from the repository root:

```bash
uv run pytest textedit
```

The suite creates an empty document of its own and closes it without saving at the end. Save your own TextEdit documents first, since the suite quits TextEdit when it finishes.

## The tests

Each test file shows one kind of window:

| File | Window | How the screen finds it |
|---|---|---|
| `test_save_sheet.py` | The Save sheet | No `window=`. A sheet is part of its document window, so the screen's lookups already include it. |
| `test_fonts_panel.py` | The Fonts panel | `window=window(title="Fonts")`. Every `ax()` and `text()` lookup on the screen searches only the panel. |

`test_text_searches_only_the_screens_window` shows the difference: `TextEdit.untitled` finds the document's title, and `Fonts.untitled` doesn't, because the title is outside the panel.

## Generate the screens

Capture both screens into one scratch module, then copy what you need into `screens.py`:

1. Press Command-S in an empty TextEdit document to open the Save sheet, then capture the document window:

   ```bash
   uv run macuitest capture TextEdit --out /tmp/textedit.py --role AXButton --role AXTextField --role AXStaticText
   ```

2. Cancel the sheet, press Command-T to open the Fonts panel, then add the panel's screen to the same module:

   ```bash
   uv run macuitest capture TextEdit --window-title Fonts --out /tmp/textedit.py --append
   ```

3. Copy the entries you need into `screens.py`. The Fonts panel's font list changes with the selected font, so `capture` skips its rows and notes how many in a comment.

## TextEdit quirks

These quirks shaped the suite, and you may meet them in other AppKit apps:

- AppKit keeps a closed sheet alive. An element that you read before the sheet closed still answers, so wait with `wait_vanish()`, which searches again on every check.
- System Events nests the sheet's controls in a splitter group: `button "Cancel" of splitter group 1 of sheet 1 of window 1`.
- The Fonts panel leaves the accessibility tree while TextEdit isn't active. Activate TextEdit before you look up its elements.
- Command-T toggles the Fonts panel. `conftest.py` closes the panel only when it's open, including a panel left open from before the run.
