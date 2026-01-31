import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

# Scenarios
scenarios('../features/world_id_integration.feature')

@given(parsers.parse('an app ID "{app_id}" and an action ID "{action_id}"'))
def sdk_params(context, app_id, action_id):
    context['app_id'] = app_id
    context['action_id'] = action_id

@when("the SDK is initialized")
def sdk_init(context):
    context['sdk'] = WorldIDSDK(app_id=context['app_id'], action_id=context['action_id'])

@then("the SDK should have the correct app ID and action ID")
def check_sdk_params(context):
    assert context['sdk'].app_id == context['app_id']
    assert context['sdk'].action_id == context['action_id']

@given("an initialized World ID SDK")
def initialized_sdk(context):
    context['app_id'] = "test_app_123"
    context['action_id'] = "test_action_abc"
    context['sdk'] = WorldIDSDK(app_id=context['app_id'], action_id=context['action_id'])

@when(parsers.parse('a user provides a valid signal "{signal}"'))
def verify_valid_signal(context, signal):
    context['verification_result'] = context['sdk'].verify_user(signal)

@then("the user should be successfully verified")
def check_verification_success(context):
    assert context['verification_result'] is True

@when("a user provides an empty signal")
def verify_empty_signal(context):
    context['verification_result'] = context['sdk'].verify_user("")

@then("the user verification should fail")
def check_verification_failure(context):
    assert context['verification_result'] is False

@when(parsers.parse('the system processes biometric data "{data}"'))
def process_data(context, data):
    context['raw_data'] = data.encode()
    context['processed_data'] = process_biometric_data(context['raw_data'])

@then("the processed data should indicate success")
def check_process_success(context):
    assert context['processed_data']['processed'] is True

@then("the processed data should contain a hash of the original data")
def check_process_hash(context):
    assert context['processed_data']['data_hash'] == hash(context['raw_data'])

@given(parsers.parse('processed biometric data from "{data}"'))
def processed_data_setup(context, data):
    context['raw_data'] = data.encode()
    context['processed_data'] = process_biometric_data(context['raw_data'])

@when("the system generates a zero-knowledge proof")
def generate_zkp(context):
    context['proof'] = generate_zero_knowledge_proof(context['processed_data'])

@then(parsers.parse('the proof should start with "{prefix}"'))
def check_proof_prefix(context, prefix):
    assert context['proof'].startswith(prefix)

@then("the proof should contain the data hash")
def check_proof_hash(context):
    assert str(context['processed_data']['data_hash']) in context['proof']

@when(parsers.parse('the system handles a successful verification with proof "{proof}"'))
def handle_success(context, proof):
    context['handle_result'] = handle_verification_result(True, proof)

@then(parsers.parse('the result status should be "{status}"'))
def check_handle_status(context, status):
    assert context['handle_result']['status'] == status

@then(parsers.parse('the result should contain the proof "{proof}"'))
def check_handle_proof(context, proof):
    assert context['handle_result']['proof'] == proof

@then("the result message should indicate success")
def check_handle_success_message(context):
    assert "success" in context['handle_result']['message'].lower()

@when("the system handles a failed verification")
def handle_failure(context):
    context['handle_result'] = handle_verification_result(False, "")

@then("the result should not contain a proof")
def check_handle_no_proof(context):
    assert context['handle_result']['proof'] is None

@then("the result message should indicate failure")
def check_handle_failure_message(context):
    assert "failed" in context['handle_result']['message'].lower()
