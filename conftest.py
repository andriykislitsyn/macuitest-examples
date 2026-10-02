"""Skip every test when the terminal lacks the permissions macuitest needs."""

import ApplicationServices
import pytest
import Quartz

PANES = "System Settings > Privacy & Security"


@pytest.fixture(autouse=True, scope="session")
def permissions():
    if not ApplicationServices.AXIsProcessTrusted():
        pytest.skip(f"Grant Accessibility to this terminal in {PANES} > Accessibility")
    if not Quartz.CGPreflightScreenCaptureAccess():
        pytest.skip(
            f"Grant Screen Recording to this terminal in {PANES} > Screen & System Audio Recording"
        )
