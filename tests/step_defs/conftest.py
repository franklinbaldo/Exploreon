# tests/step_defs/conftest.py

import pytest
from src.qr_system import DynamicQRGenerator

@pytest.fixture
def secret_key():
    """Provides a consistent secret key for QR code generation."""
    return "a_very_secret_key_for_testing"

@pytest.fixture
def qr_generator(secret_key):
    """Provides an instance of the DynamicQRGenerator."""
    return DynamicQRGenerator(secret_key=secret_key)

@pytest.fixture
def context():
    """Provides a dictionary to share state between test steps."""
    return {}
