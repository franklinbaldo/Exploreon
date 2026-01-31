Feature: Dynamic QR System
  As an event organizer
  I want to generate and verify dynamic QR codes
  So that I can ensure authentic human presence at events

  Background:
    Given a QR generator is initialized with a secret key "test_secret_key_for_qr_tests"

  Scenario: Generate a dynamic QR code
    Given an event with ID "eventXYZ789" at location "locationPQR456"
    When the organizer generates a QR code for the event with a duration of 60 seconds
    Then the QR code data should contain the event ID "eventXYZ789"
    And the QR code data should contain the location ID "locationPQR456"
    And the QR code data should have a valid signature
    And the organizer should receive a valid expiry timestamp

  Scenario: Parse QR code data
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    When the system parses the QR code data
    Then the parsed data should match the original event and location

  Scenario: Verify a valid QR code
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    When a user scans the QR code at location "locationPQR456" within the validity window
    Then the QR code should be successfully verified

  Scenario: Fail verification with wrong location
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    When a user scans the QR code at location "incorrect_location_ID"
    Then the QR code verification should fail

  Scenario: Fail verification with tampered signature
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    And the QR code signature is tampered with
    When a user scans the QR code at location "locationPQR456"
    Then the QR code verification should fail

  Scenario: Fail verification with tampered event ID
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    And the QR code event ID is changed to "tampered_event_id"
    When a user scans the QR code at location "locationPQR456"
    Then the QR code verification should fail

  Scenario: Fail verification when expired
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    When a user scans the QR code after the validity window has passed
    Then the QR code verification should fail

  Scenario: Verify QR code just before expiry
    Given a generated QR code for event "eventXYZ789" at location "locationPQR456"
    When a user scans the QR code 1 second before it expires
    Then the QR code should be successfully verified

  Scenario: Fail verification with incomplete data
    Given an incomplete QR code missing the signature field
    When a user scans the QR code at location "locationPQR456"
    Then the QR code verification should fail

  Scenario: Fail verification with malformed timestamp
    Given a QR code with a malformed timestamp "not_an_integer"
    When a user scans the QR code at location "locationPQR456"
    Then the QR code verification should fail

  Scenario: Fail verification with empty string
    Given an empty QR code string
    When a user scans the QR code at location "locationPQR456"
    Then the QR code verification should fail
