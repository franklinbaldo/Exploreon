from __future__ import annotations
from pytest_bdd import scenarios, given, when, then, parsers
import pytest
from src.sft_minting import process_verification_for_minting


scenarios('../features/sft_minting.feature')

# Step Definitions
@given("a user has a successful experience verification for a specific event and location")
def successful_verification(context):
    context['verification_status'] = 'successful'
    context['event_id'] = 'event-123'
    context['location_id'] = 'location-456'
    context['user_id'] = 'user-789'

@given("a user has an unsuccessful or invalid experience verification")
def unsuccessful_verification(context):
    context['verification_status'] = 'invalid'
    context['event_id'] = 'event-123'
    context['location_id'] = 'location-456'
    context['user_id'] = 'user-789'

@given("a user has already minted an SFT for a specific experience")
def already_minted_sft(context):
    context['verification_status'] = 'successful'
    context['event_id'] = 'event-123'
    context['location_id'] = 'location-456'
    context['user_id'] = 'user-789'
    context['minted_sfts'] = {(context['user_id'], context['event_id']): 'sft-abc'}

@when(parsers.parse("the system processes the verification for SFT minting"))
def process_verification(context):
    result = process_verification_for_minting(
        context.get('verification_status'),
        context.get('event_id'),
        context.get('location_id'),
        context.get('user_id'),
        context.get('minted_sfts')
    )
    context.update(result)


@when(parsers.parse("the system attempts to process the verification for SFT minting"))
def attempt_to_process_verification(context):
    process_verification(context)


@when(parsers.parse("the system processes another verification for the same experience"))
def process_duplicate_verification(context):
    process_verification(context)


@then("a new SFT with correct metadata should be minted for the user's account")
def verify_sft_minted_with_metadata(context):
    assert context.get('mint_result') == 'success'
    assert context.get('sft_metadata') is not None
    assert context['sft_metadata']['event'] == context['event_id']
    assert context['sft_metadata']['location'] == context['location_id']


@then("no SFT should be minted and an error should be logged")
def verify_no_sft_and_error_log(context):
    assert context.get('mint_result') == 'failure'
    assert context.get('error_log') == 'Invalid verification'


@then("no duplicate SFT should be minted and the system should recognize the duplicate")
def verify_no_duplicate_sft_and_recognition(context):
    assert context.get('mint_result') == 'duplicate'
