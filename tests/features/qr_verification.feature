Feature: QR Code Verification
  As a verification system
  I want to validate dynamic QR codes
  So that I can ensure only authorized and timely scans are accepted

  Scenario: Successful QR Code Verification
    Given a valid and fresh QR code is generated for a specific location
    When the QR code is verified at the correct location and within the validity period
    Then the verification should be successful

  Scenario: QR Code Verification Fails Due to Invalid Location
    Given a valid and fresh QR code is generated for a specific location
    When the QR code is verified at an incorrect location
    Then the verification should fail

  Scenario: QR Code Verification Fails Due to Expired Code
    Given a QR code is generated with a short validity period
    When the QR code is verified after the validity period has expired
    Then the verification should fail

  Scenario: QR Code Verification Fails Due to Tampered Signature
    Given a valid QR code is generated
    When the QR code's signature is tampered with and then verified
    Then the verification should fail
