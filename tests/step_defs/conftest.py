import pytest
from pytest_bdd import given, parsers
from src.qr_system import DynamicQRGenerator

@pytest.fixture
def secret_key():
    return "test_secret_key_for_qr_tests"

@given(parsers.parse('the QR generator is initialized with secret "{secret}"'), target_fixture="generator")
def initialized_generator(secret):
    return DynamicQRGenerator(secret_key=secret)

# Reusable context for sharing state between steps in a scenario
class ScenarioContext:
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key)

    def get(self, key, default=None):
        return self.data.get(key, default)

@pytest.fixture
def scenario_context():
    return ScenarioContext()
