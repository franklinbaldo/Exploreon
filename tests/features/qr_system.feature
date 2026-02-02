Feature: Dynamic QR Code System
  As an event organizer
  I want to generate and verify time-sensitive QR codes
  So that I can ensure only authentic visitors at the correct location and time can check in.

  Background:
    Given the QR generator is initialized with a secret key "test_secret_key_for_qr_tests"

  Scenario: Generating a valid QR code
    When a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    Then the QR code should contain the event ID "eventXYZ789"
    And the QR code should contain the location ID "locationPQR456"
    And the QR code should have a valid 16-character signature

  Scenario: Verifying a valid QR code
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    When the QR code is verified at location "locationPQR456" within the validity window
    Then the verification should be successful

  Scenario: Verifying a QR code at the wrong location
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    When the QR code is verified at location "wrong_location"
    Then the verification should fail

  Scenario: Verifying an expired QR code
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    When 70 seconds have passed since generation
    And the QR code is verified at location "locationPQR456"
    Then the verification should fail

  Scenario: Verifying a QR code with a tampered signature
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    When the QR code signature is tampered with
    And the QR code is verified at location "locationPQR456"
    Then the verification should fail
