import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Load scenarios
scenarios('../features/qr_system.feature')

# Steps
@given(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}" with {duration:d} seconds duration'), target_fixture="qr_info")
@when(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}" with {duration:d} seconds duration'), target_fixture="qr_info")
def generate_qr(generator, event_id, location_id, duration):
    qr_data, expiry_ts = generator.generate_qr_code_data(
        event_id, location_id, duration_seconds=duration
    )
    return {
        "qr_data": qr_data,
        "expiry_ts": expiry_ts,
        "event_id": event_id,
        "location_id": location_id,
        "duration": duration
    }

@given(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}"'), target_fixture="qr_info")
@when(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}"'), target_fixture="qr_info")
def generate_qr_given(generator, event_id, location_id):
    return generate_qr(generator, event_id, location_id, 60)

@then('the QR code data should follow the structured format')
def check_format(qr_info):
    qr_data = qr_info["qr_data"]
    assert qr_data.startswith("E:")
    assert "|LID:" in qr_data
    assert "|TS:" in qr_data
    assert "|S:" in qr_data

@then('the QR code data should contain the correct event and location')
def check_content(qr_info):
    qr_data = qr_info["qr_data"]
    assert f"E:{qr_info['event_id']}" in qr_data
    assert f"LID:{qr_info['location_id']}" in qr_data

@then('the expiry timestamp should be correctly calculated')
def check_expiry(qr_info):
    qr_data = qr_info["qr_data"]
    parts = dict(item.split(":", 1) for item in qr_data.split("|"))
    gen_ts = int(parts["TS"])
    assert qr_info["expiry_ts"] == gen_ts + qr_info["duration"]

@when('the QR code data is parsed', target_fixture="parsed_data")
def parse_qr(generator, qr_info):
    return generator.parse_qr_code_data(qr_info["qr_data"])

@then('the parsed data should match the original event and location')
def check_parsed_match(parsed_data, qr_info):
    assert parsed_data["event_id"] == qr_info["event_id"]
    assert parsed_data["location_id"] == qr_info["location_id"]

@then('the parsed data should include a valid timestamp and signature')
def check_parsed_fields(parsed_data):
    assert isinstance(parsed_data["timestamp"], int)
    assert len(parsed_data["signature"]) == 16

@when(parsers.parse('the QR code is verified at location "{verify_location}" after {delay:d} seconds'), target_fixture="verification_result")
def verify_qr(generator, qr_info, verify_location, delay):
    qr_data = qr_info["qr_data"]
    parts = dict(item.split(":", 1) for item in qr_data.split("|"))
    gen_ts = int(parts["TS"])
    verify_time = gen_ts + delay

    return generator.verify_qr_code_data(
        qr_data, verify_location, verify_time, validity_window_seconds=qr_info["duration"]
    )

@then(parsers.parse('the verification result should be {expected_result}'))
def check_verification_result(verification_result, expected_result):
    expected = (expected_result.lower() == 'true')
    assert verification_result == expected

@given('the QR code signature is tampered with')
def tamper_signature(qr_info):
    qr_data = qr_info["qr_data"]
    sig_marker = "|S:"
    index = qr_data.find(sig_marker) + len(sig_marker)
    qr_info["qr_data"] = qr_data[:index] + "0000000000000000"

@given(parsers.parse('the QR code event ID is changed to "{new_event_id}"'))
def tamper_event_id(qr_info, new_event_id):
    qr_data = qr_info["qr_data"]
    old_event_marker = f"E:{qr_info['event_id']}"
    new_event_marker = f"E:{new_event_id}"
    qr_info["qr_data"] = qr_data.replace(old_event_marker, new_event_marker)

@when(parsers.parse('the QR code is verified at location "{verify_location}"'), target_fixture="verification_result")
def verify_qr_no_delay(generator, qr_info, verify_location):
    return verify_qr(generator, qr_info, verify_location, 1)

@when('an empty QR code string is verified', target_fixture="verification_result")
def verify_empty_qr(generator):
    return generator.verify_qr_code_data(
        "", "some_location", int(time.time()), validity_window_seconds=60
    )
