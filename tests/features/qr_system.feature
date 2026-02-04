Feature: Dynamic QR System
  As a system administrator
  I want to generate and verify time-sensitive QR codes
  So that I can ensure authentic human presence at specific locations and events

  Scenario: Generate a valid QR code
    Given a QR generator initialized with a secret key
    When a QR code is generated for event "eventXYZ789" at location "locationPQR456"
    Then the QR code data should contain the event ID, location ID, a timestamp, and a signature

  Scenario: Verify a valid QR code
    Given a QR generator initialized with a secret key
    And a QR code generated for event "eventXYZ789" at location "locationPQR456"
    When the QR code is verified at location "locationPQR456" within the validity window
    Then the verification should be successful

  Scenario: Verification fails for incorrect location
    Given a QR generator initialized with a secret key
    And a QR code generated for event "eventXYZ789" at location "locationPQR456"
    When the QR code is verified at location "wrong_location"
    Then the verification should fail

  Scenario: Verification fails for tampered signature
    Given a QR generator initialized with a secret key
    And a QR code generated for event "eventXYZ789" at location "locationPQR456"
    When the QR code signature is tampered
    And the QR code is verified at location "locationPQR456"
    Then the verification should fail

  Scenario: Verification fails for expired QR code
    Given a QR generator initialized with a secret key
    And a QR code generated for event "eventXYZ789" at location "locationPQR456"
    When the current time is beyond the QR code validity window
    And the QR code is verified at location "locationPQR456"
    Then the verification should fail

  Scenario: Parsing malformed QR code data
    Given a QR generator initialized with a secret key
    When a malformed QR code string "E:bad|no_colon" is parsed
    Then the parsing result should be empty
