import pytest
from src.qr_system import DynamicQRGenerator

@pytest.fixture
def context():
    return {}

@pytest.fixture
def secret_key():
    return "test_secret_key_12345"

@pytest.fixture
def qr_generator(secret_key):
    return DynamicQRGenerator(secret_key=secret_key)
