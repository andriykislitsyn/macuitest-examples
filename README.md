# macuitest examples

This repository shows how to test real macOS apps with [macuitest](https://github.com/andriykislitsyn/macuitest). Each folder holds a complete suite for one app, written the way the macuitest project recommends: locators in one generated module, screenshots next to it, and tests that read like the steps a person takes.

Use these suites to see each element kind at work, or copy a folder as the starting point for your own app.

> [!WARNING]
> The tests take over your mouse and keyboard while they run. Don't type or move the mouse until a run finishes.

## What's in this repository

The repository has one folder per app:

| Folder | App | What it shows |
|---|---|---|
| [`calculator/`](calculator/) | Calculator | Every element kind: accessibility, AppleScript, screenshots, and visible text |

## Before you begin

To run the suites, you need the following:

- macOS 26 and [uv](https://docs.astral.sh/uv/).
- Two permissions for the app you run the tests from, such as Terminal or your IDE. Grant them in **System Settings > Privacy & Security**:
  - **Accessibility**, to read and control other apps.
  - **Screen & System Audio Recording**, to find elements by screenshot or by text.

After you grant a permission, quit and reopen the app you run the tests from. macOS applies the grant only to a newly started app. Until then, every test skips and names the first missing permission.

## Run a suite

1. Clone the repository and install the dependencies:

   ```bash
   git clone https://github.com/andriykislitsyn/macuitest-examples
   cd macuitest-examples
   uv sync
   ```

2. Run one app's suite:

   ```bash
   uv run pytest calculator
   ```

The suite launches the app, runs the tests, and quits the app. If the app is already open, the suite uses that window and quits the app at the end, so save your work in it first.

## How an app folder is organized

Each app folder follows the same layout:

```text
calculator/
  __init__.py              # Makes the folder a package, so app folders don't clash
  screens.py               # Screen classes: every element the tests use
  screens/calculator/      # Screenshots for image() elements, one folder per Screen class
  conftest.py              # Launches the app and resets it between tests
  test_screens.py          # Checks that every element resolves, without clicking
  test_*.py                # One file per element kind, plus an end-to-end test
```

The tests never contain locators. They read elements from `screens.py`, so when the app changes, you update one file. To generate `screens.py` for an app, see [Calculator examples](calculator/README.md).

To start a folder for your own app from a copy of `calculator/`, change the `from calculator.screens` imports to your folder's name. The screenshot folder follows the `Screen` class name in snake case, so `class TextEdit(Screen, ...)` reads its screenshots from `screens/text_edit/`.

## Continuous integration

GitHub Actions checks style with ruff on every push to `main` and on every pull request. The tests themselves run only on your Mac, because GitHub's macOS runners can't grant the Accessibility and Screen Recording permissions.

## License

MIT. See [LICENSE](LICENSE).
