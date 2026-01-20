from pytest_bdd import scenarios, given, when, then, parsers
import pytest
from src.sft_system import SFTManager

# Scenarios
scenarios('../features/sft_creation.feature')

@pytest.fixture
def context():
    return {}

@given('an event organizer has a valid event contract')
def organizer_has_contract(context):
    context['event_contract'] = "0x1234567890abcdef"
    context['sft_manager'] = SFTManager(contract_address=context['event_contract'])

@when(parsers.parse('the organizer creates SFTs for the event with a total supply of {total_supply:d} tickets'))
def create_sfts(context, total_supply):
    context['created_sfts'] = context['sft_manager'].create_sfts(total_supply)

@then(parsers.parse('{expected_supply:d} SFTs should be created for the event'))
def verify_sft_creation(context, expected_supply):
    assert len(context.get('created_sfts')) == expected_supply

@then('each SFT should be associated with the correct event contract')
def verify_sft_association(context):
    event_contract = context.get('event_contract')
    for sft in context.get('created_sfts', []):
        assert sft['contract'] == event_contract
