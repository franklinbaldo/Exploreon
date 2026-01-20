Feature: SFT Creation for Event Tickets
  As an event organizer
  I want to create Semi-Fungible Tokens (SFTs) for event tickets
  So that each ticket is a unique, verifiable digital asset.

  Scenario: Organizer creates SFTs for a new event
    Given an event organizer has a valid event contract
    When the organizer creates SFTs for the event with a total supply of 1000 tickets
    Then 1000 SFTs should be created for the event
    And each SFT should be associated with the correct event contract
