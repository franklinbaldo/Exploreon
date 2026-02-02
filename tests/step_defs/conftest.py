import pytest
from src.qr_system import DynamicQRGenerator

@pytest.fixture
def context():
    """Shared context for BDD steps."""
    return {}

@pytest.fixture
def qr_generator():
    """Fixture for DynamicQRGenerator."""
    def _generator(secret_key):
        return DynamicQRGenerator(secret_key=secret_key)
    return _generator
