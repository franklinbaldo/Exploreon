Feature: QR Code Verification
  As a verification system
  I want to validate a dynamic QR code
  So that I can ensure only authentic users with fresh, location-specific codes can gain access.

  Scenario: Successful QR Code Verification
    Given a QR code generator with a secret key
    When a valid QR code is generated for an event at a specific location
    And the QR code is verified at the correct location within the validity period
    Then the verification should be successful

  Scenario: Expired QR Code Verification
    Given a QR code generator with a secret key
    When a valid QR code is generated for an event at a specific location
    And the QR code is verified after the validity period has passed
    Then the verification should fail

  Scenario: QR Code Verification at Wrong Location
    Given a QR code generator with a secret key
    When a valid QR code is generated for an event at a specific location
    And the QR code is verified at a different location
    Then the verification should fail

  Scenario: Tampered QR Code Verification
    Given a QR code generator with a secret key
    When a QR code with a tampered signature is generated
    And the tampered QR code is verified
    Then the verification should fail
