Feature: SFT Creation for Events
  As a system administrator
  I want to create Semi-Fungible Tokens (SFTs) for new events
  So that they can be distributed to attendees as proof of experience

  Scenario: Successfully create a new SFT for an event
    Given the SFT management system is initialized
    When a new event "Crypto Summit 2024" is created with a total of 500 SFTs
    Then a new SFT collection for "Crypto Summit 2024" should be created with a supply of 500
