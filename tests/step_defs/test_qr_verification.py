# tests/step_defs/test_qr_verification.py
import time
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Load scenarios from the feature file
scenarios('../features/qr_verification.feature')

# Fixtures

@given(parsers.parse('a QR code is generated for "{event_id}" at "{location_id}" with a validity of {validity:d} seconds'), target_fixture="context")
def qr_code_generated(context, secret_key, event_id, location_id, validity):
    context.qr_generator = DynamicQRGenerator(secret_key=secret_key)
    context.generation_timestamp = int(time.time())
    context.validity = validity  # Store validity in context
    context.qr_data, _ = context.qr_generator.generate_qr_code_data(
        event_id=event_id,
        location_id=location_id,
        duration_seconds=validity
    )
    return context

@given("the verification system is ready", target_fixture="context")
def verification_system_ready(context, secret_key):
    context.qr_generator = DynamicQRGenerator(secret_key=secret_key)
    return context

@when(parsers.parse('a user presents the QR code for verification at "{location_id}" {seconds:d} seconds after it was generated'))
def present_qr_code(context, location_id, seconds):
    verification_time = context.generation_timestamp + seconds
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=context.qr_data,
        current_location_id_for_verification=location_id,
        current_time_for_verification=verification_time,
        validity_window_seconds=context.validity
    )

@when(parsers.parse('a user presents a QR code with a tampered signature for verification at "{location_id}" {seconds:d} seconds after it was generated'))
def present_tampered_signature_qr_code(context, location_id, seconds):
    tampered_qr_data = context.qr_data.rsplit('|', 1)[0] + '|S:tampered'
    verification_time = context.generation_timestamp + seconds
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data,
        current_location_id_for_verification=location_id,
        current_time_for_verification=verification_time,
        validity_window_seconds=context.validity
    )

@when(parsers.parse('a user presents a QR code with a tampered event ID for verification at "{location_id}" {seconds:d} seconds after it was generated'))
def present_tampered_event_id_qr_code(context, location_id, seconds):
    # This will result in a signature mismatch
    tampered_qr_data = context.qr_data.replace("event-123", "event-hacked")
    verification_time = context.generation_timestamp + seconds
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data,
        current_location_id_for_verification=location_id,
        current_time_for_verification=verification_time,
        validity_window_seconds=context.validity
    )

@when('a user presents a malformed QR code string for verification at any location')
def present_malformed_qr_code(context):
    malformed_qr_data = "this_is_not_a_valid_qr_code"
    verification_time = int(time.time())
    context.verification_result = context.qr_generator.verify_qr_code_data(
        qr_data_string=malformed_qr_data,
        current_location_id_for_verification="any-location",
        current_time_for_verification=verification_time,
        validity_window_seconds=60
    )

@then('the verification should be successful')
def verification_successful(context):
    assert context.verification_result is True

@then('the verification should fail')
def verification_should_fail(context):
    assert context.verification_result is False
