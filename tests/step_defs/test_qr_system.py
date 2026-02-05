import time
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

scenarios('../features/qr_system.feature')

@given('a QR generator initialized with a secret key', target_fixture='generator')
def qr_generator(secret_key):
    return DynamicQRGenerator(secret_key=secret_key)

@when(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}"'), target_fixture='qr_data')
def generate_qr(generator, event_id, location_id, context):
    qr_data, expiry_ts = generator.generate_qr_code_data(event_id, location_id)
    context.event_id = event_id
    context.location_id = location_id
    context.qr_data = qr_data
    context.expiry_ts = expiry_ts
    return qr_data

@given(parsers.parse('a QR code generated for event "{event_id}" at location "{location_id}"'))
def given_qr_generated(generator, event_id, location_id, context):
    qr_data, expiry_ts = generator.generate_qr_code_data(event_id, location_id)
    context.event_id = event_id
    context.location_id = location_id
    context.qr_data = qr_data
    context.expiry_ts = expiry_ts

@then('the QR code data should contain the event ID, location ID, a timestamp, and a signature')
def verify_qr_data_structure(context):
    parts = dict(item.split(":", 1) for item in context.qr_data.split("|"))
    assert parts["E"] == context.event_id
    assert parts["LID"] == context.location_id
    assert "TS" in parts
    assert "S" in parts
    assert len(parts["S"]) == 16

@when(parsers.parse('the QR code is verified at location "{verify_location}" within the validity window'), target_fixture='verification_result')
def verify_qr_valid_step(generator, context, verify_location):
    current_time = int(time.time())
    return generator.verify_qr_code_data(
        context.qr_data, verify_location, current_time, validity_window_seconds=60
    )

@when(parsers.parse('the QR code is verified at location "{verify_location}"'), target_fixture='verification_result')
def verify_qr_step(generator, context, verify_location):
    verify_time = getattr(context, 'verify_time', int(time.time()))
    return generator.verify_qr_code_data(
        context.qr_data, verify_location, verify_time, validity_window_seconds=60
    )

@then('the verification should be successful')
def check_verification_success(verification_result):
    assert verification_result is True

@then('the verification should fail')
def check_verification_failure(verification_result):
    assert verification_result is False

@when('the QR code signature is tampered')
def tamper_signature(context):
    sig_marker = "|S:"
    sig_start_index = context.qr_data.find(sig_marker) + len(sig_marker)
    context.qr_data = context.qr_data[:sig_start_index] + "0000000000000000"

@when('the current time is beyond the QR code validity window')
def set_expired_time(context):
    # We parse the timestamp from the QR data
    parts = dict(item.split(":", 1) for item in context.qr_data.split("|"))
    gen_time = int(parts["TS"])
    context.verify_time = gen_time + 70 # 70s is beyond 60s default window

@when(parsers.parse('a malformed QR code string "{malformed_string}" is parsed'), target_fixture='parsed_result')
def parse_malformed(generator, malformed_string):
    return generator.parse_qr_code_data(malformed_string)

@then('the parsing result should be empty')
def check_parsing_empty(parsed_result):
    assert parsed_result is None
