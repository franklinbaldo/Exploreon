import pytest

@pytest.fixture
def context():
    """A dictionary to share state between test steps."""
    return {}
