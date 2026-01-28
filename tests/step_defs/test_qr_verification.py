# tests/step_defs/test_qr_verification.py

import time
from pytest_bdd import scenarios, given, when, then

# Bind scenarios from the feature file
scenarios('../features/qr_verification.feature')


@given('a valid and fresh QR code is generated for a specific location')
def fresh_qr_code(context, qr_generator):
    context['location_id'] = "entrance_gate_1"
    context['event_id'] = "event_123"
    context['duration'] = 60  # seconds
    qr_data, _ = qr_generator.generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id'],
        duration_seconds=context['duration']
    )
    context['qr_data'] = qr_data


@given('a QR code is generated with a short validity period')
def short_validity_qr_code(context, qr_generator):
    context['location_id'] = "short_lived_gate"
    context['event_id'] = "event_456"
    context['duration'] = 1  # 1 second validity
    qr_data, _ = qr_generator.generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id'],
        duration_seconds=context['duration']
    )
    context['qr_data'] = qr_data


@given('a valid QR code is generated')
def valid_qr_code(context, qr_generator):
    context['location_id'] = "any_location"
    context['event_id'] = "any_event"
    context['duration'] = 60
    qr_data, _ = qr_generator.generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id'],
        duration_seconds=context['duration']
    )
    context['qr_data'] = qr_data


@when('the QR code is verified at the correct location and within the validity period')
def verify_at_correct_location(context, qr_generator):
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )


@when('the QR code is verified at an incorrect location')
def verify_at_incorrect_location(context, qr_generator):
    current_time = int(time.time())
    incorrect_location = "exit_gate_5"
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=incorrect_location,
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )


@when('the QR code is verified after the validity period has expired')
def verify_after_expiry(context, qr_generator):
    parsed_data = qr_generator.parse_qr_code_data(context['qr_data'])
    assert parsed_data is not None
    generation_timestamp = parsed_data['timestamp']

    # Calculate a time that is definitely after the expiry
    expired_time = generation_timestamp + context['duration'] + 1

    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=expired_time,
        validity_window_seconds=context['duration']
    )


@when("the QR code's signature is tampered with and then verified")
def verify_with_tampered_signature(context, qr_generator):
    tampered_qr_data = context['qr_data'].replace('S:', 'S:tampered')
    current_time = int(time.time())
    context['verification_result'] = qr_generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data,
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )


@then('the verification should be successful')
def check_verification_success(context):
    assert context['verification_result'] is True


@then('the verification should fail')
def check_verification_failure(context):
    assert context['verification_result'] is False
