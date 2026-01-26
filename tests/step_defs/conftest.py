# tests/step_defs/conftest.py
import pytest

class AppContext:
    """A simple container for sharing state between BDD steps."""
    def __init__(self):
        self.qr_generator = None
        self.qr_data = None
        self.generation_timestamp = None
        self.verification_result = None
        self.validity = 0  # To store the QR code's validity duration

@pytest.fixture
def context():
    """Provides a shared context object for the BDD scenarios."""
    return AppContext()

@pytest.fixture
def secret_key():
    """Provides a shared secret key for the QR generator."""
    return "a_very_secret_key"
