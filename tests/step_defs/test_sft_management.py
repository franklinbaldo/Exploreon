from pytest_bdd import scenarios, given, when, then, parsers
import pytest

from src.sft_system import SFTManager

scenarios('../features/sft_management.feature')

@pytest.fixture
def context():
    return {}

@pytest.fixture
def sft_manager():
    return SFTManager()

@given("the SFT management system is initialized")
def sft_system_initialized(sft_manager):
    assert sft_manager is not None

@when(parsers.parse('a new event "{event_name}" is created with a total of {total_sfts:d} SFTs'))
def create_event(sft_manager, context, event_name, total_sfts):
    context["event_name"] = event_name
    sft_manager.create_sft_collection(event_name, total_sfts)

@then(parsers.parse('a new SFT collection for "{event_name}" should be created with a supply of {supply:d}'))
def verify_sft_collection(sft_manager, context, event_name, supply):
    collection = sft_manager.get_sft_collection(event_name)
    assert collection is not None
    assert collection["name"] == event_name
    assert collection["supply"] == supply
