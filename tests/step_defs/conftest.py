import pytest

@pytest.fixture
def secret_key():
    return "test_secret_key_for_qr_tests"

@pytest.fixture
def context():
    class Context:
        pass
    return Context()
