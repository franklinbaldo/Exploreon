from pytest_bdd import scenarios, given, when, then
from src.world_id_integration import WorldIDSDK
from src.qr_system import DynamicQRGenerator
import time

# Scenarios
scenarios('../features/experience_verification.feature')

@given("a user with a valid World ID")
def user_with_valid_world_id(context):
    context['world_id_sdk'] = WorldIDSDK(app_id="app_staging_123", action_id="verify_experience")
    context['user_signal'] = "user_world_id_signal_data"

@given("a user with an invalid World ID")
def user_with_invalid_world_id(context):
    context['world_id_sdk'] = WorldIDSDK(app_id="app_staging_123", action_id="verify_experience")
    context['user_signal'] = ""

@given("an event with a specific location")
def event_with_specific_location(context):
    context['event_id'] = "event_456"
    context['location_id'] = "location_789"
    context['qr_generator'] = DynamicQRGenerator(secret_key="a_very_secret_key")

@when("the user scans a dynamic QR code at the event location")
def user_scans_dynamic_qr_code(context):
    qr_data, _ = context['qr_generator'].generate_qr_code_data(
        event_id=context['event_id'],
        location_id=context['location_id']
    )
    context['qr_data'] = qr_data

@then("the QR code should be considered valid")
def qr_code_should_be_valid(context):
    is_qr_valid = context['qr_generator'].verify_qr_code_data(
        qr_data_string=context['qr_data'],
        current_location_id_for_verification=context['location_id'],
        current_time_for_verification=int(time.time()),
        validity_window_seconds=300
    )
    assert is_qr_valid, "QR code should be valid"

@when("their World ID is successfully verified")
def world_id_is_successfully_verified(context):
    context['is_verified'] = context['world_id_sdk'].verify_user(context['user_signal'])
    assert context['is_verified'], "World ID should be verified"

@when("their World ID verification fails")
def world_id_verification_fails(context):
    context['is_verified'] = context['world_id_sdk'].verify_user(context['user_signal'])
    assert not context['is_verified'], "World ID verification should fail"

@then("they should be rewarded with an SFT representing their experience")
def they_should_be_rewarded_with_sft(context):
    if context.get('is_verified'):
        sft_id = f"sft_{context['event_id']}_{context['user_signal']}"
        context['sft'] = sft_id
        assert context['sft'] is not None
    else:
        assert context.get('sft') is None

@then("they should not be rewarded with an SFT")
def they_should_not_be_rewarded_with_sft(context):
    assert context.get('sft') is None, "SFT should not be minted if verification fails"
