# tests/step_defs/conftest.py
import pytest

@pytest.fixture
def context():
    """A dictionary to share state between steps."""
    return {}

@pytest.fixture
def secret_key():
    """Provides a secret key for testing."""
    return "a_very_secret_key_from_fixture"
