import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Load scenarios from the feature file
scenarios('../features/qr_system.feature')

@given("the QR system is initialized with a secret key", target_fixture="qr_generator")
def qr_system_init(secret_key):
    return DynamicQRGenerator(secret_key=secret_key)

@given(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}"'))
@when(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}"'))
def generate_qr(qr_generator, event_id, location_id, context):
    qr_data, expiry_ts = qr_generator.generate_qr_code_data(event_id, location_id)
    context["qr_data"] = qr_data
    context["expiry_ts"] = expiry_ts
    context["event_id"] = event_id
    context["location_id"] = location_id

@then("the QR code should contain the event ID, location ID, and a timestamp")
def check_qr_content(qr_generator, context):
    parsed = qr_generator.parse_qr_code_data(context["qr_data"])
    assert parsed is not None
    assert parsed["event_id"] == context["event_id"]
    assert parsed["location_id"] == context["location_id"]
    assert isinstance(parsed["timestamp"], int)

@then("the QR code should have a valid signature")
def check_qr_signature(qr_generator, context):
    parsed = qr_generator.parse_qr_code_data(context["qr_data"])
    assert len(parsed["signature"]) == 16
    # verify_qr_code_data also checks signature
    is_valid = qr_generator.verify_qr_code_data(
        context["qr_data"],
        context["location_id"],
        parsed["timestamp"]
    )
    assert is_valid is True

@when(parsers.parse('the QR code is verified at location "{verify_location}" within the validity window'))
def verify_qr_valid(qr_generator, context, verify_location):
    current_time = int(time.time())
    context["verification_result"] = qr_generator.verify_qr_code_data(
        context["qr_data"],
        verify_location,
        current_time,
        validity_window_seconds=60
    )

@then("the verification should be successful")
def check_verification_success(context):
    assert context["verification_result"] is True

@given(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}" with a short duration'))
def generate_qr_short_duration(qr_generator, event_id, location_id, context):
    # We'll use a very short duration or just simulate expiry by passing a later time to verify
    qr_data, expiry_ts = qr_generator.generate_qr_code_data(event_id, location_id, duration_seconds=1)
    context["qr_data"] = qr_data
    context["event_id"] = event_id
    context["location_id"] = location_id

@when("the QR code is verified after it has expired")
def verify_qr_expired(qr_generator, context):
    # Instead of waiting, we provide a current_time that is definitely in the future
    parsed = qr_generator.parse_qr_code_data(context["qr_data"])
    future_time = parsed["timestamp"] + 301 # Default window is usually 300, or we can specify
    context["verification_result"] = qr_generator.verify_qr_code_data(
        context["qr_data"],
        context["location_id"],
        future_time,
        validity_window_seconds=300
    )

@then("the verification should fail")
def check_verification_failure(context):
    assert context["verification_result"] is False

@when(parsers.parse('the QR code is verified at location "{verify_location}"'))
def verify_qr_location(qr_generator, context, verify_location):
    current_time = int(time.time())
    context["verification_result"] = qr_generator.verify_qr_code_data(
        context["qr_data"],
        verify_location,
        current_time
    )

@given("the QR code signature is tampered with")
def tamper_signature(context):
    qr_data = context["qr_data"]
    # Tamper signature: find "S:" and change its value
    sig_marker = "|S:"
    sig_start_index = qr_data.find(sig_marker) + len(sig_marker)
    context["qr_data"] = qr_data[:sig_start_index] + "0000000000000000"

@given(parsers.parse('the QR code event ID is changed to "{new_event_id}"'))
def tamper_event_id(context, new_event_id):
    qr_data = context["qr_data"]
    # E:old_event -> E:new_event
    old_event_part = f"E:{context['event_id']}"
    new_event_part = f"E:{new_event_id}"
    context["qr_data"] = qr_data.replace(old_event_part, new_event_part)

@when(parsers.parse('a malformed QR string "{malformed_string}" is verified at location "{verify_location}"'))
def verify_malformed(qr_generator, context, malformed_string, verify_location):
    current_time = int(time.time())
    context["verification_result"] = qr_generator.verify_qr_code_data(
        malformed_string,
        verify_location,
        current_time
    )
