Feature: QR Code Verification for Experience Proof
  As a user of the Exploreon platform
  I want to verify my presence at an event using a dynamic QR code
  So that I can receive a semi-fungible token (SFT) as proof of my experience.

  Scenario: Successful Verification with a Valid QR Code
    Given a QR code is generated for "event-123" at "location-A" with a validity of 60 seconds
    When a user presents the QR code for verification at "location-A" 30 seconds after it was generated
    Then the verification should be successful

  Scenario: Failed Verification due to Incorrect Location
    Given a QR code is generated for "event-123" at "location-A" with a validity of 60 seconds
    When a user presents the QR code for verification at "location-B" 30 seconds after it was generated
    Then the verification should fail

  Scenario: Failed Verification due to Expired QR Code
    Given a QR code is generated for "event-123" at "location-A" with a validity of 60 seconds
    When a user presents the QR code for verification at "location-A" 90 seconds after it was generated
    Then the verification should fail

  Scenario: Failed Verification due to Tampered Signature
    Given a QR code is generated for "event-123" at "location-A" with a validity of 60 seconds
    When a user presents a QR code with a tampered signature for verification at "location-A" 30 seconds after it was generated
    Then the verification should fail

  Scenario: Failed Verification due to Tampered Content
    Given a QR code is generated for "event-123" at "location-A" with a validity of 60 seconds
    When a user presents a QR code with a tampered event ID for verification at "location-A" 30 seconds after it was generated
    Then the verification should fail

  Scenario: Failed Verification with a Malformed QR Code
    Given the verification system is ready
    When a user presents a malformed QR code string for verification at any location
    Then the verification should fail
