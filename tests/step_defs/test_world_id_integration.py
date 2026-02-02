from pytest_bdd import scenarios, given, when, then, parsers
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

# Scenarios
scenarios('../features/world_id_integration.feature')

@given(parsers.parse('the World ID SDK is initialized with app ID "{app_id}" and action ID "{action_id}"'))
def initialized_sdk(context, app_id, action_id):
    context['sdk'] = WorldIDSDK(app_id=app_id, action_id=action_id)

@when(parsers.parse('a user provides a valid signal "{signal}"'))
def verify_user_valid(context, signal):
    context['verification_result'] = context['sdk'].verify_user(signal)

@when('a user provides an empty signal')
def verify_user_empty(context):
    context['verification_result'] = context['sdk'].verify_user("")

@when(parsers.parse('raw biometric data "{raw_data}" is processed'))
@given(parsers.parse('raw biometric data "{raw_data}" is processed'))
def process_biometric(context, raw_data):
    # The source code expects bytes
    context['processed_data'] = process_biometric_data(raw_data.encode())

@when('a zero-knowledge proof is generated')
def generate_zkp(context):
    context['proof'] = generate_zero_knowledge_proof(context['processed_data'])

@when(parsers.parse('a successful verification result is handled with proof "{proof}"'))
def handle_success(context, proof):
    context['final_result'] = handle_verification_result(True, proof)

@when('a failed verification result is handled')
def handle_failure(context):
    context['final_result'] = handle_verification_result(False, "")

@then('the user should be successfully verified')
def check_user_verified(context):
    assert context['verification_result'] is True

@then('the user verification should fail')
def check_user_not_verified(context):
    assert context['verification_result'] is False

@then('the processed data should indicate success')
def check_process_success(context):
    assert context['processed_data']['processed'] is True

@then('it should contain a data hash')
def check_data_hash(context):
    assert 'data_hash' in context['processed_data']

@then(parsers.parse('the proof should start with "{prefix}"'))
def check_proof_prefix(context, prefix):
    assert context['proof'].startswith(prefix)

@then('it should contain the data hash')
def check_proof_contains_hash(context):
    assert str(context['processed_data']['data_hash']) in context['proof']

@then(parsers.parse('the status should be "{status}"'))
def check_status(context, status):
    assert context['final_result']['status'] == status

@then(parsers.parse('the result should contain the proof "{proof}"'))
def check_result_proof(context, proof):
    assert context['final_result']['proof'] == proof

@then('the result should not contain a proof')
def check_result_no_proof(context):
    assert context['final_result']['proof'] is None
