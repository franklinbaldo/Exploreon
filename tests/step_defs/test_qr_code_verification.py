# tests/step_defs/test_qr_code_verification.py

import time
from pytest_bdd import scenarios, given, when, then
from freezegun import freeze_time

scenarios('../features/qr_code_verification.feature')

# Step Definitions

@given('a QR code is generated for a specific event and location')
def generate_qr_code(context, qr_generator):
    context['event_id'] = "event123"
    context['location_id'] = "location456"
    context['duration'] = 60  # seconds
    with freeze_time("2023-01-01 12:00:00"):
        qr_data, _ = qr_generator.generate_qr_code_data(
            context['event_id'], context['location_id'], duration_seconds=context['duration']
        )
        context['qr_data'] = qr_data

@when('a user presents the QR code for verification at the correct location and within the valid time window')
def present_qr_code_for_verification(context, qr_generator):
    with freeze_time("2023-01-01 12:00:30"):
        current_time = int(time.time())
        is_valid = qr_generator.verify_qr_code_data(
            context['qr_data'],
            context['location_id'],
            current_time,
            validity_window_seconds=context['duration']
        )
        context['is_valid'] = is_valid

@when('a user presents the QR code for verification at an incorrect location')
def present_qr_code_at_incorrect_location(context, qr_generator):
    with freeze_time("2023-01-01 12:00:30"):
        current_time = int(time.time())
        is_valid = qr_generator.verify_qr_code_data(
            context['qr_data'],
            "incorrect_location",
            current_time,
            validity_window_seconds=context['duration']
        )
        context['is_valid'] = is_valid

@when('a user presents a QR code with a tampered signature for verification')
def present_tampered_qr_code(context, qr_generator):
    # Parse the QR data to isolate the signature
    parsed_data = qr_generator.parse_qr_code_data(context['qr_data'])
    if parsed_data:
        # Create a tampered signature that is guaranteed to be incorrect
        tampered_signature = "0" * len(parsed_data["signature"])
        # Reconstruct the QR data string with the tampered signature
        tampered_qr_data = (
            f"E:{parsed_data['event_id']}|"
            f"LID:{parsed_data['location_id']}|"
            f"TS:{parsed_data['timestamp']}|"
            f"S:{tampered_signature}"
        )
        context['qr_data'] = tampered_qr_data

    with freeze_time("2023-01-01 12:00:30"):
        current_time = int(time.time())
        is_valid = qr_generator.verify_qr_code_data(
            context['qr_data'],
            context['location_id'],
            current_time,
            validity_window_seconds=context['duration']
        )
        context['is_valid'] = is_valid


@when('a user presents the QR code for verification after the validity period has expired')
def present_expired_qr_code(context, qr_generator):
    with freeze_time("2023-01-01 12:01:30"):  # 90 seconds after generation
        current_time = int(time.time())
        is_valid = qr_generator.verify_qr_code_data(
            context['qr_data'],
            context['location_id'],
            current_time,
            validity_window_seconds=context['duration']
        )
        context['is_valid'] = is_valid

@then('the system successfully verifies the QR code')
def check_successful_verification(context):
    assert context['is_valid'] is True

@then('the system fails to verify the QR code')
def check_failed_verification(context):
    assert context['is_valid'] is False
