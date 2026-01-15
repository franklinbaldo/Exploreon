# tests/step_defs/test_qr_code_verification.py

import time
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Fixtures

@pytest.fixture
def secret_key():
    """Provides a consistent secret key for tests."""
    return "a_very_secret_key_for_bdd_tests"

@pytest.fixture
def qr_generator(secret_key):
    """Initializes the DynamicQRGenerator with the secret key."""
    return DynamicQRGenerator(secret_key=secret_key)

@pytest.fixture
def event_context():
    """A dictionary to share state between test steps."""
    return {}

# Scenario Definition

@scenario(
    '../features/qr_code_verification.feature',
    'Successful verification of a valid QR code'
)
def test_successful_qr_code_verification():
    """BDD test for successful QR code verification."""
    pass

# Step Definitions

@given("a QR code generator is initialized with a secret key")
def qr_generator_initialized(qr_generator):
    """Checks if the QR generator fixture is created."""
    assert qr_generator is not None

@given(parsers.parse('an event with ID "{event_id}" is happening at location "{location_id}"'))
def event_details(event_context, event_id, location_id):
    """Stores the event ID and location ID in the context."""
    event_context["event_id"] = event_id
    event_context["location_id"] = location_id

@when("a dynamic QR code is generated for the event and location")
def generate_qr_code(qr_generator, event_context):
    """Generates a QR code and stores its data in the context."""
    qr_data, _ = qr_generator.generate_qr_code_data(
        event_id=event_context["event_id"],
        location_id=event_context["location_id"],
        duration_seconds=60
    )
    event_context["qr_data"] = qr_data

@when("the user presents the QR code for verification at the correct location within the validity period")
def verify_qr_code(qr_generator, event_context):
    """Verifies the QR code at the correct location and stores the result."""
    current_time = int(time.time())
    is_valid = qr_generator.verify_qr_code_data(
        qr_data_string=event_context["qr_data"],
        current_location_id_for_verification=event_context["location_id"],
        current_time_for_verification=current_time,
        validity_window_seconds=300
    )
    event_context["verification_result"] = is_valid

@then("the QR code should be successfully verified")
def check_verification_success(event_context):
    """Asserts that the verification result is True."""
    assert event_context["verification_result"] is True
