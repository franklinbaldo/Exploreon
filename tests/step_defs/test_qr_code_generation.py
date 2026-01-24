# tests/step_defs/test_qr_code_generation.py
from freezegun import freeze_time
from pytest_bdd import scenarios, given, when, then, parsers
from src.qr_system import DynamicQRGenerator

# Scenarios
scenarios('../features/qr_code_generation.feature')

@given(parsers.parse('an event with ID "{event_id}" at location "{location_id}"'))
def event_details(context, event_id, location_id):
    context['event_id'] = event_id
    context['location_id'] = location_id

@given('a QR code generator initialized with a secret key')
def qr_generator(context, secret_key):
    context['secret_key'] = secret_key
    context['generator'] = DynamicQRGenerator(secret_key=context['secret_key'])

@when(parsers.parse('the organizer generates a QR code for the event with a {duration:d}-second duration'))
@freeze_time("2024-01-01 12:00:00")
def generate_qr_code(context, duration):
    qr_data, expiry_ts = context['generator'].generate_qr_code_data(
        context['event_id'], context['location_id'], duration_seconds=duration
    )
    context['qr_data'] = qr_data
    context['expiry_ts'] = expiry_ts
    # Parse the data to use for more robust assertions in the 'then' steps
    parsed_data = context['generator'].parse_qr_code_data(qr_data)
    context['parsed_qr_data'] = parsed_data
    context['generation_timestamp'] = parsed_data['timestamp']

@then('a QR code is generated')
def qr_code_generated(context):
    assert 'qr_data' in context and context['qr_data'] is not None
    assert 'expiry_ts' in context and context['expiry_ts'] is not None

@then(parsers.parse('the QR code data contains the event ID "{event_id}"'))
def qr_code_contains_event_id(context, event_id):
    assert context['parsed_qr_data']['event_id'] == event_id

@then(parsers.parse('the QR code data contains the location ID "{location_id}"'))
def qr_code_contains_location_id(context, location_id):
    assert context['parsed_qr_data']['location_id'] == location_id

@then(parsers.parse('the QR code has an expiry timestamp approximately {duration:d} seconds in the future'))
def qr_code_has_expiry(context, duration):
    # With freezegun, the test is now deterministic and the check can be exact.
    expected_expiry = context['generation_timestamp'] + duration
    assert context['expiry_ts'] == expected_expiry
