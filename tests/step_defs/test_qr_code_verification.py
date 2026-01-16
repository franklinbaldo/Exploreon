
import pytest
from pytest_bdd import scenario, given, when, then
import time
from src.qr_system import DynamicQRGenerator

# Constants for tests
SECRET_KEY = "test_secret_key"
EVENT_ID = "event123"
LOCATION_ID = "location456"
VALIDITY_DURATION = 60  # seconds

@pytest.fixture
def qr_generator():
    """Provides a DynamicQRGenerator instance."""
    return DynamicQRGenerator(secret_key=SECRET_KEY)

@pytest.fixture
def qr_code_context():
    """Provides a dictionary to store context between steps."""
    return {}

# Scenario Implementations

@scenario('../features/qr_code_verification.feature', 'Successful Verification with a Valid QR Code')
def test_successful_verification():
    pass

@scenario('../features/qr_code_verification.feature', 'Failed Verification due to Incorrect Location')
def test_failed_verification_incorrect_location():
    pass

@scenario('../features/qr_code_verification.feature', 'Failed Verification due to Expired QR Code')
def test_failed_verification_expired_qr_code():
    pass

@scenario('../features/qr_code_verification.feature', 'Failed Verification due to Tampered QR Code')
def test_failed_verification_tampered_qr_code():
    pass

@scenario('../features/qr_code_verification.feature', 'Failed Verification due to Malformed QR Code')
def test_failed_verification_malformed_qr_code():
    pass

# Step Definitions

@given("a QR code is generated for a specific event and location", target_fixture="qr_code_context")
def qr_code_generated_for_event_and_location(qr_generator, qr_code_context):
    qr_data, _ = qr_generator.generate_qr_code_data(EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_DURATION)
    qr_code_context["qr_data"] = qr_data
    return qr_code_context

@given("a QR code is generated with a specific validity period", target_fixture="qr_code_context")
def qr_code_generated_with_validity_period(qr_generator, qr_code_context):
    qr_data, _ = qr_generator.generate_qr_code_data(EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_DURATION)
    qr_code_context["qr_data"] = qr_data
    return qr_code_context

@given("a valid QR code", target_fixture="qr_code_context")
def valid_qr_code(qr_generator, qr_code_context):
    qr_data, _ = qr_generator.generate_qr_code_data(EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_DURATION)
    qr_code_context["qr_data"] = qr_data
    return qr_code_context

@given("a malformed QR code", target_fixture="qr_code_context")
def malformed_qr_code(qr_code_context):
    qr_code_context["qr_data"] = "this is not a valid qr code"
    return qr_code_context

@when("I present the QR code for verification at the correct location within the validity period")
def present_qr_code_for_verification_correct(qr_generator, qr_code_context):
    current_time = int(time.time())
    result = qr_generator.verify_qr_code_data(qr_code_context["qr_data"], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_DURATION)
    qr_code_context["verification_result"] = result

@when("I present the QR code for verification at an incorrect location")
def present_qr_code_for_verification_incorrect_location(qr_generator, qr_code_context):
    current_time = int(time.time())
    result = qr_generator.verify_qr_code_data(qr_code_context["qr_data"], "incorrect_location", current_time, validity_window_seconds=VALIDITY_DURATION)
    qr_code_context["verification_result"] = result

@when("I present the QR code for verification after the validity period has passed")
def present_qr_code_for_verification_expired(qr_generator, qr_code_context):
    # Simulate time passing
    current_time = int(time.time()) + VALIDITY_DURATION + 1
    result = qr_generator.verify_qr_code_data(qr_code_context["qr_data"], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_DURATION)
    qr_code_context["verification_result"] = result

@when("the QR code is tampered with")
def tamper_qr_code(qr_code_context):
    qr_data = qr_code_context["qr_data"]
    tampered_qr_data = qr_data.replace("S:", "S:tampered")
    qr_code_context["qr_data"] = tampered_qr_data

@when("I present the tampered QR code for verification")
def present_tampered_qr_code_for_verification(qr_generator, qr_code_context):
    current_time = int(time.time())
    result = qr_generator.verify_qr_code_data(qr_code_context["qr_data"], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_DURATION)
    qr_code_context["verification_result"] = result

@when("I present the malformed QR code for verification")
def present_malformed_qr_code_for_verification(qr_generator, qr_code_context):
    current_time = int(time.time())
    result = qr_generator.verify_qr_code_data(qr_code_context["qr_data"], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_DURATION)
    qr_code_context["verification_result"] = result

@then("the verification should be successful")
def verification_should_be_successful(qr_code_context):
    assert qr_code_context["verification_result"] is True

@then("the verification should fail")
def verification_should_fail(qr_code_context):
    assert qr_code_context["verification_result"] is False
