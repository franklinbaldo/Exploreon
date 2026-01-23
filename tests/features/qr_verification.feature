Feature: Dynamic QR Code Verification
  As a verification system
  I want to validate dynamic QR codes
  So that I can ensure only authorized users gain access at the correct time and location

  Scenario: Successful Verification of a Valid QR Code
    Given a dynamic QR code generator is initialized with a secret key
    And a valid dynamic QR code is generated for an event and location
    When the QR code is verified at the correct location within the validity period
    Then the verification should be successful

  Scenario: Verification Fails with Incorrect Location
    Given a dynamic QR code generator is initialized with a secret key
    And a valid dynamic QR code is generated for an event and location
    When the QR code is verified at an incorrect location
    Then the verification should fail

  Scenario: Verification Fails for Expired QR Code
    Given a dynamic QR code generator is initialized with a secret key
    And a dynamic QR code is generated with a short validity period
    When the QR code is verified after the validity period has expired
    Then the verification should fail

  Scenario: Verification Fails for Tampered QR Code
    Given a dynamic QR code generator is initialized with a secret key
    And a valid dynamic QR code is generated for an event and location
    When the QR code's data is tampered with
    And the tampered QR code is verified
    Then the verification should fail
