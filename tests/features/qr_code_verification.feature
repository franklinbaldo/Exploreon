Feature: QR Code Verification for Secure Event Access
  As a system administrator
  I want to ensure that QR codes are verified securely
  So that only valid users can gain access to events.

  Scenario: Successful QR Code Verification
    Given a QR code is generated for a specific event and location
    When a user presents the QR code for verification at the correct location and within the valid time window
    Then the system successfully verifies the QR code

  Scenario: Verification Fails Due to Incorrect Location
    Given a QR code is generated for a specific event and location
    When a user presents the QR code for verification at an incorrect location
    Then the system fails to verify the QR code

  Scenario: Verification Fails Due to Tampered Signature
    Given a QR code is generated for a specific event and location
    When a user presents a QR code with a tampered signature for verification
    Then the system fails to verify the QR code

  Scenario: Verification Fails Due to Expired QR Code
    Given a QR code is generated for a specific event and location
    When a user presents the QR code for verification after the validity period has expired
    Then the system fails to verify the QR code
