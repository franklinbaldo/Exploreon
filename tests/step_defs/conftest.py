# tests/step_defs/conftest.py
import pytest

# Fixture for a shared secret key
@pytest.fixture
def secret_key():
    """Provides a consistent secret key for tests."""
    return "a_very_secret_key_for_testing_bdd"

# Fixture for a shared context object to pass state between steps
@pytest.fixture
def context():
    """Provides a shared dictionary to store state across BDD steps."""
    return {}
