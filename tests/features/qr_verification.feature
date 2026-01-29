# tests/features/qr_verification.feature
Feature: QR Code Verification
  As a verification system
  I want to generate and validate time-sensitive QR codes
  So that I can ensure secure, authentic, and timely user experiences at specific locations.

  Scenario: Generate a valid QR code
    Given a QR code generator initialized with a secret key
    When a QR code is generated for an event and location
    Then the QR code data should contain the event ID, location ID, a timestamp, and a signature.

  Scenario: Verify a valid QR code
    Given a valid QR code is generated
    When the QR code is verified at the correct location within the validity window
    Then the verification should be successful.

  Scenario: Fail verification for an expired QR code
    Given a valid QR code is generated
    When the QR code is verified after the validity window has passed
    Then the verification should fail.

  Scenario: Fail verification for a QR code at the wrong location
    Given a valid QR code is generated for a specific location
    When the QR code is verified at a different location
    Then the verification should fail.

  Scenario: Fail verification for a tampered QR code
    Given a QR code with a tampered signature
    When the QR code is verified
    Then the verification should fail.
