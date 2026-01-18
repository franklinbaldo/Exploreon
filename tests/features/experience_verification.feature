Feature: Experience Verification and SFT Minting
  As a user
  I want to verify my presence at an event
  So that I can receive a unique Semi-Fungible Token (SFT) as proof of my experience

  Scenario: Successful Experience Verification and SFT Minting
    Given a user with a valid World ID
    And an event with a specific location
    When the user scans a dynamic QR code at the event location
    Then the QR code should be considered valid
    When their World ID is successfully verified
    Then they should be rewarded with an SFT representing their experience

  Scenario: Failed World ID Verification
    Given a user with an invalid World ID
    And an event with a specific location
    When the user scans a dynamic QR code at the event location
    Then the QR code should be considered valid
    When their World ID verification fails
    Then they should not be rewarded with an SFT
