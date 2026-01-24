Feature: QR Code Generation for Event Verification
  As an event organizer
  I want to generate a dynamic and secure QR code for a specific event and location
  So that I can verify a user's presence in a tamper-proof way

  Scenario: Generate a valid QR code for an event
    Given an event with ID "event-123" at location "location-456"
    And a QR code generator initialized with a secret key
    When the organizer generates a QR code for the event with a 60-second duration
    Then a QR code is generated
    And the QR code data contains the event ID "event-123"
    And the QR code data contains the location ID "location-456"
    And the QR code has an expiry timestamp approximately 60 seconds in the future
