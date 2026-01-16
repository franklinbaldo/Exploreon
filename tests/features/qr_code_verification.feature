Feature: QR Code Verification
  As a user of the Exploreon platform,
  I want to use a dynamic QR code to verify my presence at an event,
  So that I can securely receive a digital collectible (SFT).

  Scenario: Successful Verification with a Valid QR Code
    Given a QR code is generated for a specific event and location
    When I present the QR code for verification at the correct location within the validity period
    Then the verification should be successful

  Scenario: Failed Verification due to Incorrect Location
    Given a QR code is generated for a specific event and location
    When I present the QR code for verification at an incorrect location
    Then the verification should fail

  Scenario: Failed Verification due to Expired QR Code
    Given a QR code is generated with a specific validity period
    When I present the QR code for verification after the validity period has passed
    Then the verification should fail

  Scenario: Failed Verification due to Tampered QR Code
    Given a valid QR code
    When the QR code is tampered with
    And I present the tampered QR code for verification
    Then the verification should fail

  Scenario: Failed Verification due to Malformed QR Code
    Given a malformed QR code
    When I present the malformed QR code for verification
    Then the verification should fail
