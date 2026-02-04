from pytest_bdd import scenarios, given, when, then, parsers
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

scenarios('../features/world_id_integration.feature')

@given(parsers.parse('a World ID SDK initialized with app ID "{app_id}" and action ID "{action_id}"'), target_fixture='sdk')
def world_id_sdk(app_id, action_id):
    return WorldIDSDK(app_id=app_id, action_id=action_id)

@when(parsers.parse('the user is verified with signal "{signal}"'), target_fixture='verification_status')
def verify_user(sdk, signal):
    return sdk.verify_user(signal)

@when('the user is verified with signal ""', target_fixture='verification_status')
def verify_user_empty(sdk):
    return sdk.verify_user("")

@then('the verification status should be successful')
def check_verification_status_success(verification_status):
    assert verification_status is True

@then('the verification status should be failure')
def check_verification_status_failure(verification_status):
    assert verification_status is False

@when(parsers.parse('biometric data "{raw_data}" is processed'), target_fixture='processed_data')
def process_biometric(raw_data, context):
    data_bytes = raw_data.encode()
    context.raw_data_hash = hash(data_bytes)
    return process_biometric_data(data_bytes)

@then('the processed data should indicate success and include a data hash')
def verify_processed_data(processed_data, context):
    assert processed_data["processed"] is True
    assert processed_data["data_hash"] == context.raw_data_hash

@given(parsers.parse('processed biometric data from "{raw_data}"'), target_fixture='processed_data')
def given_processed_biometric(raw_data, context):
    data_bytes = raw_data.encode()
    context.raw_data_hash = hash(data_bytes)
    return process_biometric_data(data_bytes)

@when('a zero-knowledge proof is generated', target_fixture='zk_proof')
def generate_zkp(processed_data):
    return generate_zero_knowledge_proof(processed_data)

@then('the proof should be valid and contain the data hash')
def verify_zk_proof(zk_proof, context):
    assert zk_proof.startswith("zkp_")
    assert str(context.raw_data_hash) in zk_proof

@when(parsers.parse('a successful verification result is handled with proof "{proof}"'), target_fixture='handle_result')
def handle_success(proof):
    return handle_verification_result(True, proof)

@then(parsers.parse('the result status should be "{status}"'))
def verify_result_status(handle_result, status):
    assert handle_result["status"] == status

@then(parsers.parse('the result should contain the proof "{proof}"'))
def verify_result_proof(handle_result, proof):
    assert handle_result["proof"] == proof

@when('a failed verification result is handled', target_fixture='handle_result')
def handle_failure():
    return handle_verification_result(False, "")

@then('the result should not contain a proof')
def verify_result_no_proof(handle_result):
    assert handle_result["proof"] is None
