# tests/step_defs/test_qr_verification.py

import pytest
import time
from pytest_bdd import scenarios, given, when, then, parsers

from src.qr_system import DynamicQRGenerator

# Load all scenarios from the feature file
scenarios('../features/qr_verification.feature')

# Fixtures to share context between steps

@pytest.fixture
def context():
    """A dictionary to share state between steps"""
    return {}

# Step Definitions

@given('a QR code generator with a secret key')
def qr_code_generator(context):
    """Initializes the DynamicQRGenerator with a secret key."""
    context['secret_key'] = "a_very_secret_key_for_bdd_tests"
    context['generator'] = DynamicQRGenerator(secret_key=context['secret_key'])
    assert context['generator'] is not None

@when('a valid QR code is generated for an event at a specific location')
def generate_valid_qr_code(context):
    """Generates a QR code for a predefined event and location."""
    context['event_id'] = "event-123"
    context['location_id'] = "location-abc"
    context['duration'] = 60  # seconds
    qr_data, _ = context['generator'].generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id'],
        duration_seconds=context['duration']
    )
    context['qr_data'] = qr_data

@when('a QR code with a tampered signature is generated')
def generate_tampered_qr_code(context):
    """Generates a valid QR code and then tampers with its signature."""
    context['event_id'] = "event-123"
    context['location_id'] = "location-abc"
    context['duration'] = 60
    qr_data, _ = context['generator'].generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id'],
        duration_seconds=context['duration']
    )
    # Tamper the signature
    context['qr_data'] = qr_data[:-16] + "0123456789abcdef"

@when('the QR code is verified at the correct location within the validity period')
def verify_at_correct_location_and_time(context):
    """Verifies the QR code at the correct location within its validity window."""
    current_time = int(time.time())
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )

@when('the QR code is verified after the validity period has passed')
def verify_after_validity_period(context):
    """Simulates time passing and verifies the QR code after it has expired."""
    # Get the generation timestamp from the QR data string
    parsed_qr_data = context['generator'].parse_qr_code_data(context['qr_data'])
    generation_time = parsed_qr_data['timestamp']

    expired_time = generation_time + context['duration'] + 5 # 5 seconds after expiry
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=expired_time,
        validity_window_seconds=context['duration']
    )

@when('the QR code is verified at a different location')
def verify_at_wrong_location(context):
    """Verifies the QR code at a different location."""
    current_time = int(time.time())
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification="wrong-location-xyz",
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )
@when('the tampered QR code is verified')
def verify_tampered_code(context):
    """Verifies the tampered QR code."""
    current_time = int(time.time())
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )

@then('the verification should be successful')
def check_verification_success(context):
    """Asserts that the verification result is True."""
    assert context.get('verification_result') is True

@then('the verification should fail')
def check_verification_failure(context):
    """Asserts that the verification result is False."""
    assert context.get('verification_result') is False
