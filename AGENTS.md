# Agent notes for macuitest-examples

These suites take over the user's mouse and keyboard and quit the apps they drive. Run a suite only when the user approves that run. These need no approval, since they only read: `uv run pytest calculator/test_screens.py`, `uv run python -m macuitest.locators tree <app>` without `--activate`, and `uv run python -m macuitest.locators check <app>/screens.py`. `tree` ships after macuitest 0.8.0, so it works once `uv.lock` picks up that release.

## Commands

```bash
uv sync
uv run ruff check && uv run ruff format --check
uv run pytest <app>
```

CI runs ruff only. GitHub's macOS runners can't grant Accessibility or Screen Recording, so the tests run only on a Mac.

## Adding an app folder

1. Explore with `tree <app>`, then generate a module with `capture <app> --out <app>/screens.py`. Each `capture` run writes one module, so capture a sheet or panel into a scratch file and merge it by hand.
2. Edit the module: delete entries the tests don't need, and replace any locator that encodes state, such as an identifier holding the current mode. Comment each edit, since the edits are part of what the repo shows.
3. Run `check <app>/screens.py` until it reports nothing.
4. Write a `conftest.py` with a session fixture that launches the app, waits for its window, and quits it at the end, like `calculator/conftest.py` and `textedit/conftest.py`.
5. Add the folder's `README.md` and a row in the root README table. Docs follow the Google developer documentation style guide.

## Rules for fixtures and tests

- Call `Application.activate()` before every hotkey or typed input. It raises unless the app comes to the front, so keys can't land in another app, such as the user's editor.
- Never type into or save the user's documents. Create your own, leave them empty, and close them with `saving no`.
- A fixture closes whatever it opened, such as a sheet or panel, even when the test fails. Check before toggling: Command-T on an open Fonts panel closes it.
- Tests read elements and helpers, such as `display_value()`, from `screens.py`, and never contain locators.
