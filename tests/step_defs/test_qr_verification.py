# tests/step_defs/test_qr_verification.py
import time
from datetime import datetime
from pytest_bdd import scenarios, given, when, then
from freezegun import freeze_time
from src.qr_system import DynamicQRGenerator

# Load scenarios
scenarios('../features/qr_verification.feature')

@given('a dynamic QR code generator is initialized with a secret key')
def qr_generator(context):
    context.qr_generator = DynamicQRGenerator(secret_key=context.secret_key)
    assert context.qr_generator is not None

@given('a valid dynamic QR code is generated for an event and location')
def valid_qr_code(context):
    context.qr_data, _ = context.qr_generator.generate_qr_code_data(
        event_id=context.event_id,
        location_id=context.location_id,
        duration_seconds=60
    )
    assert context.qr_data is not None

@given('a dynamic QR code is generated with a short validity period')
def qr_code_short_validity(context):
    context.qr_data, _ = context.qr_generator.generate_qr_code_data(
        event_id=context.event_id,
        location_id=context.location_id,
        duration_seconds=1  # 1-second validity
    )
    assert context.qr_data is not None

@when('the QR code is verified at the correct location within the validity period')
def verify_correct_location_and_time(context):
    current_time = int(time.time())
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=context.qr_data,
        current_location_id_for_verification=context.location_id,
        current_time_for_verification=current_time,
        validity_window_seconds=60
    )

@when('the QR code is verified at an incorrect location')
def verify_incorrect_location(context):
    current_time = int(time.time())
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=context.qr_data,
        current_location_id_for_verification="wrong-location",
        current_time_for_verification=current_time,
        validity_window_seconds=60
    )

@when('the QR code is verified after the validity period has expired')
def verify_after_expiry(context):
    parsed_data = context.qr_generator.parse_qr_code_data(context.qr_data)
    generation_timestamp = parsed_data['timestamp']

    # Freeze time to be 2 seconds after the QR code was generated.
    # The QR code has a 1-second validity, so this is after expiry.
    verification_time = datetime.fromtimestamp(generation_timestamp + 2)

    with freeze_time(verification_time):
        context.verification_result = context.qr_generator.verify_qr_code_data(
            qr_data_string=context.qr_data,
            current_location_id_for_verification=context.location_id,
            current_time_for_verification=int(time.time()),
            validity_window_seconds=1
        )

@when("the QR code's data is tampered with")
def tamper_qr_code(context):
    # Tamper with the event ID to invalidate the signature
    context.qr_data = context.qr_data.replace(f"E:{context.event_id}", "E:tampered-event")

@when('the tampered QR code is verified')
def verify_tampered_code(context):
    current_time = int(time.time())
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=context.qr_data,
        current_location_id_for_verification=context.location_id,
        current_time_for_verification=current_time,
        validity_window_seconds=60
    )

@then('the verification should be successful')
def then_verification_successful(context):
    assert context.verification_result is True

@then('the verification should fail')
def then_verification_fails(context):
    assert context.verification_result is False
