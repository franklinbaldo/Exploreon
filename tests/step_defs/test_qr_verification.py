# tests/step_defs/test_qr_verification.py

import time
from pytest_bdd import scenarios, given, when, then
import pytest

from src.qr_system import DynamicQRGenerator

# Constants for tests
EVENT_ID = "event-123"
LOCATION_ID = "location-456"
VALID_DURATION = 60  # seconds

# Link the feature file to the test file
scenarios('../features/qr_code_verification.feature')

# Step Definitions

@given('a QR code is generated for an event and location')
def qr_code(context, qr_generator):
    context['qr_data'], _ = qr_generator.generate_qr_code_data(
        event_id=EVENT_ID,
        location_id=LOCATION_ID,
        duration_seconds=VALID_DURATION
    )

@given('a QR code is generated for an event and location with a specific duration')
def qr_code_with_duration(context, qr_generator):
    context['qr_data'], _ = qr_generator.generate_qr_code_data(
        event_id=EVENT_ID,
        location_id=LOCATION_ID,
        duration_seconds=VALID_DURATION
    )
    context['duration'] = VALID_DURATION

@given('the system is ready for QR verification')
def system_ready(context):
    context['verification_result'] = None

@when('a user presents the QR code for verification at the correct location within the validity period')
def present_qr_code_at_correct_location(context, qr_generator):
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=current_time,
        validity_window_seconds=VALID_DURATION
    )

@when('a user presents the QR code for verification at a different location')
def present_qr_code_at_wrong_location(context, qr_generator):
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification="wrong-location",
        current_time_for_verification=current_time,
        validity_window_seconds=VALID_DURATION
    )

@when('a user presents the QR code for verification after the validity period has expired')
def present_expired_qr_code(context, qr_generator):
    parsed_data = qr_generator.parse_qr_code_data(context['qr_data'])
    assert parsed_data is not None, "Failed to parse QR data"
    generation_time = parsed_data['timestamp']
    expired_time = generation_time + context['duration'] + 10 # 10 seconds after expiry
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=expired_time,
        validity_window_seconds=context['duration']
    )

@when('a user presents a tampered version of the QR code for verification')
def present_tampered_qr_code(context, qr_generator):
    tampered_qr_data = context['qr_data'].replace('S:', 'S:tampered')
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data,
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=current_time,
        validity_window_seconds=VALID_DURATION
    )

@when('a user presents a malformed QR code for verification')
def present_malformed_qr_code(context, qr_generator):
    malformed_qr_data = "this-is-not-a-valid-qr-code"
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=malformed_qr_data,
        current_location_id_for_verification=LOCATION_ID,
        current_time_for_verification=current_time,
        validity_window_seconds=VALID_DURATION
    )

@then('the QR code should be successfully verified.')
def check_successful_verification(context):
    assert context['verification_result'] is True

@then('the QR code verification should fail.')
def check_failed_verification(context):
    assert context['verification_result'] is False
