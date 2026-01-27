Feature: QR Code Verification for Event Access
  As a system administrator
  I want to ensure that QR codes are securely verified
  So that only valid users can gain access to events at the correct location and time.

  Scenario: Successful QR Code Verification
    Given a QR code is generated for an event and location
    When a user presents the QR code for verification at the correct location within the validity period
    Then the QR code should be successfully verified.

  Scenario: Verification at a Wrong Location
    Given a QR code is generated for an event and location
    When a user presents the QR code for verification at a different location
    Then the QR code verification should fail.

  Scenario: Verification of an Expired QR Code
    Given a QR code is generated for an event and location with a specific duration
    When a user presents the QR code for verification after the validity period has expired
    Then the QR code verification should fail.

  Scenario: Verification of a Tampered QR Code
    Given a QR code is generated for an event and location
    When a user presents a tampered version of the QR code for verification
    Then the QR code verification should fail.

  Scenario: Verification of a Malformed QR Code
    Given the system is ready for QR verification
    When a user presents a malformed QR code for verification
    Then the QR code verification should fail.
