import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

scenarios('../features/world_id_integration.feature')

@given(parsers.parse('an app ID "{app_id}" and an action ID "{action_id}"'), target_fixture="ids")
def set_ids(app_id, action_id):
    return {"app_id": app_id, "action_id": action_id}

@when('the World ID SDK is initialized', target_fixture="sdk")
def init_sdk(ids):
    return WorldIDSDK(app_id=ids["app_id"], action_id=ids["action_id"])

@then('the SDK should have the correct app ID and action ID')
def check_sdk_ids(sdk, ids):
    assert sdk.app_id == ids["app_id"]
    assert sdk.action_id == ids["action_id"]

@given(parsers.parse('the World ID SDK is initialized with app ID "{app_id}" and action ID "{action_id}"'), target_fixture="sdk")
def init_sdk_given(app_id, action_id):
    return WorldIDSDK(app_id=app_id, action_id=action_id)

@when(parsers.parse('a user is verified with signal "{signal}"'), target_fixture="verification_status")
def verify_user(sdk, signal):
    return sdk.verify_user(signal)

@when('a user is verified with an empty signal', target_fixture="verification_status")
def verify_user_empty(sdk):
    return sdk.verify_user("")

@then(parsers.parse('the verification status should be {expected_status}'))
def check_verification_status(verification_status, expected_status):
    expected = (expected_status.lower() == 'true')
    assert verification_status == expected

@when(parsers.parse('raw biometric data "{data}" is processed'), target_fixture="biometric_info")
def process_data(data):
    raw_data = data.encode()
    processed_data = process_biometric_data(raw_data)
    return {"raw_data": raw_data, "processed_data": processed_data}

@then('the processed data should indicate success')
def check_processed_success(biometric_info):
    assert biometric_info["processed_data"]["processed"] is True

@then('the processed data should contain a hash of the raw data')
def check_processed_hash(biometric_info):
    assert biometric_info["processed_data"]["data_hash"] == hash(biometric_info["raw_data"])

@given(parsers.parse('raw biometric data "{data}" has been processed'), target_fixture="biometric_info")
def process_data_given(data):
    return process_data(data)

@when('a zero-knowledge proof is generated', target_fixture="proof")
def generate_proof(biometric_info):
    return generate_zero_knowledge_proof(biometric_info["processed_data"])

@then(parsers.parse('the proof should start with "{prefix}"'))
def check_proof_prefix(proof, prefix):
    assert proof.startswith(prefix)

@then('the proof should contain the data hash')
def check_proof_content(proof, biometric_info):
    assert str(biometric_info["processed_data"]["data_hash"]) in proof

@when(parsers.parse('a successful verification is handled with proof "{proof}"'), target_fixture="final_result")
def handle_success(proof):
    return handle_verification_result(True, proof)

@then(parsers.parse('the final result status should be "{status}"'))
def check_final_status(final_result, status):
    assert final_result["status"] == status

@then(parsers.parse('the result should contain the proof "{proof}"'))
def check_final_proof(final_result, proof):
    assert final_result["proof"] == proof

@then('the result message should indicate success')
def check_final_message_success(final_result):
    assert "success" in final_result["message"].lower()

@when('a failed verification is handled', target_fixture="final_result")
def handle_failure():
    return handle_verification_result(False, "")

@then('the result should not contain a proof')
def check_final_no_proof(final_result):
    assert final_result["proof"] is None

@then('the result message should indicate failure')
def check_final_message_failure(final_result):
    assert "failed" in final_result["message"].lower()
