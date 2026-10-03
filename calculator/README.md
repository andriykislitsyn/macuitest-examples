# Calculator examples

This suite computes 7 × 6 = 42 in Calculator once for each macuitest element kind, then once more with the kinds mixed. Compare the test files to see how each kind finds and drives the same keys.

## Requirements

The suite expects the following setup:

- macOS 26. Calculator's accessibility tree can change with any macOS release.
- Calculator in Basic mode. If it's in another mode, the input tests skip and ask you to switch with **View > Basic**.

## Run the suite

Run the whole suite from the repository root:

```bash
uv run pytest calculator
```

After a macOS update, run the read-only check first. It confirms that every accessibility, AppleScript, screenshot, and text element still resolves, and it doesn't click anything:

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

## Generate a screens module

To generate a module like `screens.py` for your own app, follow these steps:

1. Open the app, and bring the window you want to test to the front.
2. Capture the window. Replace `Your App` with the app's name as the Dock shows it, and `your_app` with your folder:

   ```bash
   uv run python -m macuitest.locators capture "Your App" --out your_app/screens.py --role AXButton --role AXGroup --role AXScrollArea
   ```

   The command writes a `Screen` class with an `ax()` entry for each element it can identify, else an `image()` entry, and a screenshot of each element in `your_app/screens/<screen>/`. Leave out `--role` to capture every kind of element.

3. Edit the generated module. The edits in this folder's `screens.py` show the usual ones, each with a comment:
   - `display` finds the text inside the input view with `.child()`, since the text has no identifier.
   - `mode` matches the button's description, since its generated identifier encodes the current mode.
   - The `image()`, `applescript()`, and `text()` entries reuse the same keys for the other examples.
   - Capture also generated two unnamed groups and the sidebar button. The tests don't need them, so their entries and screenshots are gone. The full keypad stays, so you can try other calculations.

4. Check that every declared screenshot exists and that no screenshot is left over:

   ```bash
   uv run python -m macuitest.locators check your_app/screens.py
   ```

## Refresh after a Calculator update

When a macOS update changes Calculator, refresh the module:

1. Run `test_screens.py` to see which elements no longer resolve.
2. Capture into a scratch file, so that you keep your edits. `--force` replaces the scratch files from an earlier refresh:

   ```bash
   uv run python -m macuitest.locators capture Calculator --out /tmp/calculator.py --role AXButton --role AXGroup --role AXScrollArea --force
   ```

   The screenshots land in `/tmp/calculator/calculator/`.

3. Copy the changed locators into `calculator/screens.py` and the changed screenshots into `calculator/screens/calculator/`, then run `check` again.

## Calculator quirks

These quirks shaped the suite, and you may meet them in other SwiftUI apps:

- The display's value starts with an invisible left-to-right mark (U+200E). `display_value()` in `screens.py` removes it.
- System Events reads each key's `description` as `"button"` and can't read its `AXDescription`. AppleScript locators match `value of attribute "AXIdentifier"` instead.
- Apple Vision doesn't read single characters reliably, so `text()` rejects them. `test_text.py` types its input and waits for the two-digit result with `Calculator.result`.
- The decimal key follows your region's format, such as `,` instead of `.`, so no test uses it.
- Calculator reports no accessibility window until it's active. `conftest.py` activates it, waits for the window, and activates it again before each input test, so typed keys can't land in another app.
