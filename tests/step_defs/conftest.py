# tests/step_defs/conftest.py
import pytest

class AppContext:
    """A context object for sharing state between BDD steps."""
    def __init__(self):
        self.qr_generator = None
        self.secret_key = "a-very-secret-key"
        self.event_id = "test-event"
        self.location_id = "test-location"
        self.qr_data = None
        self.verification_result = None

@pytest.fixture
def context():
    """Provides a shared context for BDD scenarios."""
    return AppContext()
