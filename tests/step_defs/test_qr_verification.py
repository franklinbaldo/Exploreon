# tests/step_defs/test_qr_verification.py

import time
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Constants
EVENT_ID = "event123"
LOCATION_ID = "location456"
VALIDITY_WINDOW = 60  # seconds

# Scenarios
scenarios('../features/qr_verification.feature')

@given('a QR code generator initialized with a secret key')
def qr_generator_fixture(qr_generator):
    return qr_generator

@when('a QR code is generated for an event and location')
def generate_qr_code(qr_generator, context):
    qr_data, expiry = qr_generator.generate_qr_code_data(EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_WINDOW)
    context['qr_data'] = qr_data
    context['expiry'] = expiry

@then('the QR code data should contain the event ID, location ID, a timestamp, and a signature.')
def validate_qr_code_structure(context, qr_generator):
    parsed_data = qr_generator.parse_qr_code_data(context['qr_data'])
    assert parsed_data is not None
    assert parsed_data['event_id'] == EVENT_ID
    assert parsed_data['location_id'] == LOCATION_ID
    assert isinstance(parsed_data['timestamp'], int)
    assert 'signature' in parsed_data

@given('a valid QR code is generated')
def valid_qr_code(context, qr_generator):
    context['qr_data'], _ = qr_generator.generate_qr_code_data(
        EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_WINDOW
    )

@when('the QR code is verified at the correct location within the validity window')
def verify_valid_qr_code(context, qr_generator):
    current_time = int(time.time())
    is_valid = qr_generator.verify_qr_code_data(
        context['qr_data'], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_WINDOW
    )
    context['is_valid'] = is_valid

@then('the verification should be successful.')
def check_verification_success(context):
    assert context['is_valid'] is True

@when('the QR code is verified after the validity window has passed')
def verify_expired_qr_code(context, qr_generator):
    parsed_data = qr_generator.parse_qr_code_data(context['qr_data'])
    expired_time = parsed_data['timestamp'] + VALIDITY_WINDOW + 5
    is_valid = qr_generator.verify_qr_code_data(
        context['qr_data'], LOCATION_ID, expired_time, validity_window_seconds=VALIDITY_WINDOW
    )
    context['is_valid'] = is_valid

@then('the verification should fail.')
def check_verification_failure(context):
    assert context['is_valid'] is False

@given('a valid QR code is generated for a specific location')
def qr_code_for_specific_location(context, qr_generator):
    context['qr_data'], _ = qr_generator.generate_qr_code_data(
        EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_WINDOW
    )

@when('the QR code is verified at a different location')
def verify_at_wrong_location(context, qr_generator):
    wrong_location = "location789"
    current_time = int(time.time())
    is_valid = qr_generator.verify_qr_code_data(
        context['qr_data'], wrong_location, current_time, validity_window_seconds=VALIDITY_WINDOW
    )
    context['is_valid'] = is_valid

@given('a QR code with a tampered signature')
def tampered_qr_code(context, qr_generator):
    qr_data, _ = qr_generator.generate_qr_code_data(
        EVENT_ID, LOCATION_ID, duration_seconds=VALIDITY_WINDOW
    )
    # Tamper the signature
    parts = qr_data.split('|')
    parts[-1] = "S:tamperedsignature"
    context['qr_data'] = '|'.join(parts)

@when('the QR code is verified')
def verify_tampered_qr_code(context, qr_generator):
    current_time = int(time.time())
    is_valid = qr_generator.verify_qr_code_data(
        context['qr_data'], LOCATION_ID, current_time, validity_window_seconds=VALIDITY_WINDOW
    )
    context['is_valid'] = is_valid
