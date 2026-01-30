Feature: Dynamic QR Code Verification
  As a verification system
  I want to generate and validate time-sensitive QR codes
  So that I can ensure only authorized users gain access at specific locations and times.

  Scenario: Successful QR Code Generation
    Given a QR code generator initialized with a secret key
    When a QR code is generated for an event and location
    Then the QR code data should contain the event ID, location ID, a timestamp, and a signature.

  Scenario: Successful QR Code Verification
    Given a valid QR code is generated for an event and location
    When the QR code is verified at the correct location within the validity window
    Then the verification should be successful.

  Scenario: QR Code Verification Failure (Wrong Location)
    Given a valid QR code is generated for an event and location
    When the QR code is verified at a different location
    Then the verification should fail.

  Scenario: QR Code Verification Failure (Expired)
    Given a valid QR code is generated for an event and location
    When the QR code is verified at the correct location after the validity window has passed
    Then the verification should fail.

  Scenario: QR Code Verification Failure (Tampered Signature)
    Given a valid QR code is generated for an event and location
    When the QR code's signature is tampered with
    And the QR code is verified
    Then the verification should fail.

  Scenario: QR Code Verification Failure (Tampered Content)
    Given a valid QR code is generated for an event and location
    When the QR code's event ID is tampered with
    And the QR code is verified
    Then the verification should fail due to a signature mismatch.

  Scenario: QR Code Verification Failure (Malformed Data)
    Given a QR code generator initialized with a secret key
    When an attempt is made to verify a malformed QR string
    Then the verification should fail.
