import time
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Scenarios
scenarios('../features/qr_system.feature')

@given(parsers.parse('the QR generator is initialized with a secret key "{secret_key}"'))
def initialized_generator(context, secret_key):
    context['generator'] = DynamicQRGenerator(secret_key=secret_key)

@given(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}" with {duration:d} seconds duration'))
@when(parsers.parse('a QR code is generated for event "{event_id}" at location "{location_id}" with {duration:d} seconds duration'))
def generate_qr(context, event_id, location_id, duration):
    qr_data, expiry_ts = context['generator'].generate_qr_code_data(
        event_id=event_id,
        location_id=location_id,
        duration_seconds=duration
    )
    context['qr_data'] = qr_data
    context['expiry_ts'] = expiry_ts
    context['event_id'] = event_id
    context['location_id'] = location_id
    context['duration'] = duration
    # Store generation time by parsing it back from the QR data for deterministic testing
    parsed = context['generator'].parse_qr_code_data(qr_data)
    context['generation_time'] = parsed['timestamp']

@when(parsers.parse('the QR code is verified at location "{verification_location}" within the validity window'))
def verify_qr_valid_window(context, verification_location):
    # Use current time that is guaranteed to be within window
    current_time = context['generation_time'] + 1
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=verification_location,
        current_time_for_verification=current_time,
        validity_window_seconds=context['duration']
    )

@when(parsers.parse('{seconds:d} seconds have passed since generation'))
def time_passes(context, seconds):
    context['verification_time'] = context['generation_time'] + seconds

@when(parsers.parse('the QR code is verified at location "{verification_location}"'))
def verify_qr_at_location(context, verification_location):
    v_time = context.get('verification_time', context['generation_time'] + 1)
    context['verification_result'] = context['generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=verification_location,
        current_time_for_verification=v_time,
        validity_window_seconds=context['duration']
    )

@when('the QR code signature is tampered with')
def tamper_signature(context):
    qr_data = context['qr_data']
    sig_marker = "|S:"
    sig_start_index = qr_data.find(sig_marker) + len(sig_marker)
    context['qr_data'] = qr_data[:sig_start_index] + "0000000000000000"

@then(parsers.parse('the QR code should contain the event ID "{event_id}"'))
def check_event_id(context, event_id):
    parsed = context['generator'].parse_qr_code_data(context['qr_data'])
    assert parsed['event_id'] == event_id

@then(parsers.parse('the QR code should contain the location ID "{location_id}"'))
def check_location_id(context, location_id):
    parsed = context['generator'].parse_qr_code_data(context['qr_data'])
    assert parsed['location_id'] == location_id

@then('the QR code should have a valid 16-character signature')
def check_signature(context):
    parsed = context['generator'].parse_qr_code_data(context['qr_data'])
    assert len(parsed['signature']) == 16

@then('the verification should be successful')
def check_verification_success(context):
    assert context['verification_result'] is True

@then('the verification should fail')
def check_verification_failure(context):
    assert context['verification_result'] is False
