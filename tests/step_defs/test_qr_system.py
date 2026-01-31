import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Scenarios
scenarios('../features/qr_system.feature')

# Shared Steps (could also be in conftest.py if used across multiple features)

@given(parsers.parse('a QR generator is initialized with a secret key "{secret}"'))
def qr_generator_init(context, secret):
    context['generator'] = DynamicQRGenerator(secret_key=secret)
    context['secret'] = secret

@given(parsers.parse('an event with ID "{event_id}" at location "{location_id}"'))
def event_setup(context, event_id, location_id):
    context['event_id'] = event_id
    context['location_id'] = location_id

@when(parsers.parse('the organizer generates a QR code for the event with a duration of {duration:d} seconds'))
def generate_qr(context, duration):
    qr_data, expiry_ts = context['generator'].generate_qr_code_data(
        context['event_id'], context['location_id'], duration_seconds=duration
    )
    context['qr_data'] = qr_data
    context['expiry_ts'] = expiry_ts
    context['duration'] = duration

@then(parsers.parse('the QR code data should contain the event ID "{event_id}"'))
def check_event_id(context, event_id):
    assert f"E:{event_id}" in context['qr_data']

@then(parsers.parse('the QR code data should contain the location ID "{location_id}"'))
def check_location_id(context, location_id):
    assert f"LID:{location_id}" in context['qr_data']

@then("the QR code data should have a valid signature")
def check_signature(context):
    parts = dict(item.split(":", 1) for item in context['qr_data'].split("|"))
    assert len(parts["S"]) == 16

@then("the organizer should receive a valid expiry timestamp")
def check_expiry_timestamp(context):
    parts = dict(item.split(":", 1) for item in context['qr_data'].split("|"))
    expected_expiry = int(parts["TS"]) + context['duration']
    assert context['expiry_ts'] == expected_expiry

# Scenarios: Parse QR code data
@given(parsers.parse('a generated QR code for event "{event_id}" at location "{location_id}"'))
def generated_qr(context, event_id, location_id):
    context['event_id'] = event_id
    context['location_id'] = location_id
    qr_data, expiry_ts = context['generator'].generate_qr_code_data(
        event_id, location_id, duration_seconds=60
    )
    context['qr_data'] = qr_data
    context['expiry_ts'] = expiry_ts
    context['duration'] = 60

@when("the system parses the QR code data")
def parse_qr(context):
    context['parsed_data'] = context['generator'].parse_qr_code_data(context['qr_data'])

@then("the parsed data should match the original event and location")
def check_parsed_data(context):
    assert context['parsed_data'] is not None
    assert context['parsed_data']['event_id'] == context['event_id']
    assert context['parsed_data']['location_id'] == context['location_id']

# Scenarios: Verification
@when(parsers.parse('a user scans the QR code at location "{location_id}" within the validity window'))
def verify_qr_success(context, location_id):
    current_verify_time = int(time.time())
    context['verification_result'] = context['generator'].verify_qr_code_data(
        context['qr_data'], location_id, current_verify_time, validity_window_seconds=context['duration']
    )

@then("the QR code should be successfully verified")
def check_verification_success(context):
    assert context['verification_result'] is True

@when(parsers.parse('a user scans the QR code at location "{location_id}"'))
def verify_qr_at_location(context, location_id):
    current_verify_time = int(time.time())
    context['verification_result'] = context['generator'].verify_qr_code_data(
        context['qr_data'], location_id, current_verify_time, validity_window_seconds=context['duration']
    )

@then("the QR code verification should fail")
def check_verification_failure(context):
    assert context['verification_result'] is False

@given("the QR code signature is tampered with")
def tamper_signature(context):
    sig_marker = "|S:"
    sig_start_index = context['qr_data'].find(sig_marker) + len(sig_marker)
    context['qr_data'] = context['qr_data'][:sig_start_index] + "0000000000000000"

@given(parsers.parse('the QR code event ID is changed to "{new_event_id}"'))
def tamper_event_id(context, new_event_id):
    event_marker = f"E:{context['event_id']}"
    context['qr_data'] = context['qr_data'].replace(event_marker, f"E:{new_event_id}")

@when("a user scans the QR code after the validity window has passed")
def verify_qr_expired(context):
    parts = dict(item.split(":", 1) for item in context['qr_data'].split("|"))
    time_of_qr_generation = int(parts["TS"])
    expired_verify_time = time_of_qr_generation + context['duration'] + 10
    context['verification_result'] = context['generator'].verify_qr_code_data(
        context['qr_data'], context['location_id'], expired_verify_time, validity_window_seconds=context['duration']
    )

@when(parsers.parse('a user scans the QR code {seconds:d} second before it expires'))
def verify_qr_near_expiry(context, seconds):
    parts = dict(item.split(":", 1) for item in context['qr_data'].split("|"))
    time_of_qr_generation = int(parts["TS"])
    valid_verify_time = time_of_qr_generation + context['duration'] - seconds
    context['verification_result'] = context['generator'].verify_qr_code_data(
        context['qr_data'], context['location_id'], valid_verify_time, validity_window_seconds=context['duration']
    )

@given("an incomplete QR code missing the signature field")
def incomplete_qr(context):
    timestamp = int(time.time())
    context['event_id'] = "eventXYZ789"
    context['location_id'] = "locationPQR456"
    context['duration'] = 60
    context['qr_data'] = f"E:{context['event_id']}|LID:{context['location_id']}|TS:{timestamp}"

@given(parsers.parse('a QR code with a malformed timestamp "{timestamp}"'))
def malformed_timestamp_qr(context, timestamp):
    context['event_id'] = "eventXYZ789"
    context['location_id'] = "locationPQR456"
    context['duration'] = 60
    context['qr_data'] = f"E:{context['event_id']}|LID:{context['location_id']}|TS:{timestamp}|S:1234567890abcdef"

@given("an empty QR code string")
def empty_qr_string(context):
    context['qr_data'] = ""
    context['location_id'] = "locationPQR456"
    context['duration'] = 60
