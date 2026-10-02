# Calculator examples

This suite computes 7 × 6 = 42 in Calculator once for each macuitest element kind, then once more with the kinds mixed. Compare the test files to see how each kind finds and drives the same keys.

## Requirements

The suite expects the following setup:

- macOS 26. Calculator's layout changed in macOS 15, and its accessibility tree can change again with any release.
- Calculator in Basic mode. If it's in another mode, the suite skips and asks you to switch with **View > Basic**.
- A 2x (Retina) main display for `test_image.py`. The screenshots were captured at 2x, so the test skips on a 1x main display.

## Run the suite

Run the whole suite from the repository root:

```bash
uv run pytest calculator
```

After a macOS update, run the read-only check first. It confirms that every element still resolves, and it doesn't click anything:

```bash
uv run pytest calculator/test_screens.py
```

## The tests

Each test file shows one way to find elements:

| File | Finds elements by | Good for |
|---|---|---|
| `test_native.py` | Accessibility identifier, with `ax()` | Most native controls. Fast, and independent of how the app looks. |
| `test_applescript.py` | AppleScript locator, with `applescript()` | Apps that you already script through System Events. |
| `test_image.py` | Screenshot, with `image()` | Custom-drawn controls that expose no accessibility attributes. |
| `test_text.py` | Visible text, with `text()` and Apple Vision | Labels that you'd rather not screenshot. |
| `test_end_to_end.py` | All of the above | A realistic mix, each kind where it fits best. |

## How `screens.py` was made

You can make a module like `screens.py` for your own app the same way:

1. Open Calculator in Basic mode.
2. Capture its window:

   ```bash
   uv run python -m macuitest.locators capture Calculator --out calculator/screens.py --role AXButton --role AXGroup --role AXScrollArea
   ```

   The command writes a `Screen` class with an `ax()` entry for each element, and a screenshot of each element in `calculator/screens/calculator/`.

3. Edit the generated module. The edits in this folder are commented in `screens.py`:
   - The display has no identifier, so `display` finds the text inside the input view with `.child()`.
   - The mode button's generated identifier encodes the current mode, so `mode` matches its description instead.
   - The `image()`, `applescript()`, and `text()` entries reuse the same keys for the other examples.
   - Generated entries without a useful label, two unnamed groups and the sidebar button, were deleted with their screenshots. The full keypad stays, so you can try other calculations.

4. Check that every declared screenshot exists and that no screenshot is left over:

   ```bash
   uv run python -m macuitest.locators check calculator/screens.py
   ```

## Refresh after a Calculator update

When a macOS update changes Calculator, refresh the module:

1. Run `test_screens.py` to see which elements no longer resolve.
2. Capture into a scratch file, so that you keep your edits:

   ```bash
   uv run python -m macuitest.locators capture Calculator --out /tmp/calculator.py --role AXButton --role AXGroup --role AXScrollArea
   ```

3. Copy the changed locators and screenshots into `calculator/`, then run `check` again.

## Calculator quirks

These quirks shaped the suite, and you may meet them in other SwiftUI apps:

- The display's value starts with an invisible left-to-right mark (U+200E). `display_value()` in `screens.py` removes it.
- System Events reads each key's `description` as "button" and can't read its `AXDescription`. AppleScript locators match `value of attribute "AXIdentifier"` instead.
- Apple Vision doesn't read single characters reliably, so `text()` rejects them. `test_text.py` types its input and reads only the two-digit result.
- The decimal key follows your region's format, such as `,` instead of `.`, so no test uses it.
- Calculator reports no accessibility window until it's active. `conftest.py` activates it and waits for the window.
