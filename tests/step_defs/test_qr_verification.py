# tests/step_defs/test_qr_verification.py

import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.qr_system import DynamicQRGenerator

# Constants for test data
EVENT_ID = "event_123"
LOCATION_ID = "location_456"
VALIDITY_DURATION = 60  # seconds

# Load all scenarios from the feature file
scenarios('../features/qr_verification.feature')


@pytest.fixture
def qr_generator(secret_key):
    """Provides a DynamicQRGenerator instance initialized with a secret key."""
    return DynamicQRGenerator(secret_key=secret_key)


@given("a QR code generator initialized with a secret key")
def qr_generator_initialized(qr_generator, context):
    """Initializes the QR generator and stores it in the context."""
    context['qr_generator'] = qr_generator


@when("a QR code is generated for an event and location")
def generate_qr_code(context):
    """Generates a QR code and stores the data and expiry in the context."""
    generator = context['qr_generator']
    qr_data, expiry_ts = generator.generate_qr_code_data(
        event_id=EVENT_ID,
        location_id=LOCATION_ID,
        duration_seconds=VALIDITY_DURATION
    )
    context['qr_data'] = qr_data
    context['expiry_ts'] = expiry_ts


@then("the QR code data should contain the event ID, location ID, a timestamp, and a signature.")
def validate_qr_code_data_structure(context, qr_generator):
    """Asserts that the generated QR code data has the correct structure."""
    qr_data = context['qr_data']

    # Parse the data to check its components
    parsed_data = qr_generator.parse_qr_code_data(qr_data)
    assert parsed_data is not None, "QR data could not be parsed."

    # Check content and format
    assert parsed_data['event_id'] == EVENT_ID
    assert parsed_data['location_id'] == LOCATION_ID
    assert isinstance(parsed_data['timestamp'], int)
    assert 'signature' in parsed_data
    assert isinstance(parsed_data['signature'], str)
    assert len(parsed_data['signature']) == 16, "Signature length is incorrect."


# --- Steps for Verification Scenarios ---

@given("a valid QR code is generated for an event and location")
def valid_qr_code_generated(context, qr_generator):
    """A setup step that generates a valid QR code and stores it."""
    context['qr_generator'] = qr_generator
    qr_data, _ = qr_generator.generate_qr_code_data(
        event_id=EVENT_ID,
        location_id=LOCATION_ID,
        duration_seconds=VALIDITY_DURATION
    )
    context['qr_data'] = qr_data


@when("the QR code is verified at the correct location within the validity window")
def verify_at_correct_location_and_time(context):
    """Simulates verifying the QR code at the right place and shortly after generation."""
    generator = context['qr_generator']
    parsed_data = generator.parse_qr_code_data(context['qr_data'])
    # Simulate verification happening 10 seconds after generation
    verification_time = parsed_data['timestamp'] + 10

    result = generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=verification_time,
        validity_window_seconds=VALIDITY_DURATION
    )
    context['verification_result'] = result


@then("the verification should be successful.")
def assert_verification_successful(context):
    """Asserts that the verification result was True."""
    assert context.get('verification_result') is True, "Verification was expected to succeed but failed."


@when("the QR code is verified at a different location")
def verify_at_different_location(context):
    """Simulates verifying the QR code at the wrong location."""
    generator = context['qr_generator']
    parsed_data = generator.parse_qr_code_data(context['qr_data'])
    # Simulate verification happening 10 seconds after generation
    verification_time = parsed_data['timestamp'] + 10

    result = generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification="wrong_location", # Use a different location
        current_time_for_verification=verification_time,
        validity_window_seconds=VALIDITY_DURATION
    )
    context['verification_result'] = result


@then("the verification should fail.")
def assert_verification_failed(context):
    """Asserts that the verification result was False."""
    assert context.get('verification_result') is False, "Verification was expected to fail but succeeded."


@when("the QR code is verified at the correct location after the validity window has passed")
def verify_after_expiry(context):
    """Simulates verifying the QR code after it has expired."""
    generator = context['qr_generator']
    parsed_data = generator.parse_qr_code_data(context['qr_data'])
    # Simulate verification time well after the validity window
    expired_time = parsed_data['timestamp'] + VALIDITY_DURATION + 5

    result = generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=expired_time,
        validity_window_seconds=VALIDITY_DURATION
    )
    context['verification_result'] = result


@when("the QR code's signature is tampered with")
def tamper_qr_signature(context):
    """Modifies the signature part of the QR code data string."""
    original_qr_data = context['qr_data']
    # Find the signature part and replace it with a fake one
    sig_marker = "|S:"
    sig_start_index = original_qr_data.find(sig_marker) + len(sig_marker)
    tampered_qr_data = original_qr_data[:sig_start_index] + "a_fake_signature"
    context['qr_data'] = tampered_qr_data


@when("the QR code is verified")
def qr_code_is_verified(context):
    """A generic verification step for tampered scenarios."""
    generator = context['qr_generator']
    # Use a fixed, valid timestamp for verification to isolate tampering as the failure reason.
    # Parsing might fail if the timestamp itself is tampered, so handle that.
    try:
        parsed_data = generator.parse_qr_code_data(context['qr_data'])
        verification_time = parsed_data.get('timestamp', int(time.time())) + 10
    except (ValueError, AttributeError):
        verification_time = int(time.time())

    result = generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=verification_time,
        validity_window_seconds=VALIDITY_DURATION
    )
    context['verification_result'] = result


@when("the QR code's event ID is tampered with")
def tamper_qr_event_id(context):
    """Modifies the event ID part of the QR code data string."""
    original_qr_data = context['qr_data']
    tampered_qr_data = original_qr_data.replace(f"E:{EVENT_ID}", "E:tampered_event")
    context['qr_data'] = tampered_qr_data


@then("the verification should fail due to a signature mismatch.")
def assert_verification_failed_signature_mismatch(context):
    """Asserts verification failure, specifically noting the signature mismatch reason."""
    assert context.get('verification_result') is False, "Verification should fail for tampered content."

# --- Steps for Malformed Data Scenario ---

@when("an attempt is made to verify a malformed QR string")
def attempt_to_verify_malformed_string(context):
    """Simulates verifying a QR string that is empty or badly structured."""
    generator = context['qr_generator']
    malformed_qr_string = "this_is_not_a_valid_qr_string"

    result = generator.verify_qr_code_data(
        qr_data_string=malformed_qr_string,
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=int(time.time()),
        validity_window_seconds=VALIDITY_DURATION
    )
    context['verification_result'] = result
