# tests/step_defs/conftest.py

import pytest
from src.qr_system import DynamicQRGenerator

@pytest.fixture
def qr_generator():
    """Provides a DynamicQRGenerator instance."""
    secret_key = "a_very_secret_key_for_bdd"
    return DynamicQRGenerator(secret_key=secret_key)

@pytest.fixture
def context():
    """Provides a dictionary to share state between steps."""
    return {}
