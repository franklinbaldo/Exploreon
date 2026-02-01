import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

scenarios('../features/world_id_integration.feature')

@when(parsers.parse('the World ID SDK is initialized with app ID "{app_id}" and action ID "{action_id}"'))
def sdk_init(app_id, action_id, context):
    context["sdk"] = WorldIDSDK(app_id=app_id, action_id=action_id)

@then("the SDK should have the correct app ID and action ID")
def check_sdk_init(context):
    assert context["sdk"].app_id == "app_123"
    assert context["sdk"].action_id == "action_abc"

@given("the World ID SDK is initialized")
def sdk_init_given(context):
    context["sdk"] = WorldIDSDK(app_id="app_123", action_id="action_abc")

@when(parsers.parse('a user provides a valid signal "{user_signal}"'))
def verify_user(context, user_signal):
    context["verification_status"] = context["sdk"].verify_user(user_signal)

@then("the user verification should be successful")
def check_verify_user(context):
    assert context["verification_status"] is True

@when(parsers.parse('biometric data "{raw_data}" is processed'))
def process_biometric(context, raw_data):
    context["raw_data"] = raw_data.encode()
    context["processed_data"] = process_biometric_data(context["raw_data"])

@then("the processed data should be marked as processed")
def check_processed_mark(context):
    assert context["processed_data"]["processed"] is True

@then("it should contain a hash of the original data")
def check_processed_hash(context):
    assert context["processed_data"]["data_hash"] == hash(context["raw_data"])

@given("biometric data has been processed")
def process_biometric_given(context):
    context["raw_data"] = b"raw_biometric_bytes"
    context["processed_data"] = process_biometric_data(context["raw_data"])

@when("a zero-knowledge proof is generated")
def generate_zkp(context):
    context["proof"] = generate_zero_knowledge_proof(context["processed_data"])

@then(parsers.parse('the proof should start with "{prefix}"'))
def check_proof_prefix(context, prefix):
    assert context["proof"].startswith(prefix)

@then("it should contain the data hash")
def check_proof_hash(context):
    assert str(context["processed_data"]["data_hash"]) in context["proof"]

@when(parsers.parse('a successful verification result is handled with proof "{proof}"'))
def handle_success(context, proof):
    context["result"] = handle_verification_result(True, proof)

@then(parsers.parse('the status should be "{status}"'))
def check_status(context, status):
    assert context["result"]["status"] == status

@then("the result should contain the proof")
def check_result_proof(context):
    assert context["result"]["proof"] is not None

@then("the message should indicate success")
def check_message_success(context):
    assert "success" in context["result"]["message"].lower()

@when("a failed verification result is handled")
def handle_failure(context):
    context["result"] = handle_verification_result(False, "")

@then("the result should not contain a proof")
def check_result_no_proof(context):
    assert context["result"]["proof"] is None

@then("the message should indicate failure")
def check_message_failure(context):
    assert "failed" in context["result"]["message"].lower()
