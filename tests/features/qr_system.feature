Feature: Dynamic QR System
  As a system administrator
  I want to generate and verify time-sensitive QR codes
  So that I can ensure authentic human presence at specific locations and events

  Background:
    Given the QR generator is initialized with secret "test_secret_key_for_qr_tests"

  @core
  Scenario: Generate a dynamic QR code
    When a QR code is generated for event "eventXYZ789" at location "locationPQR456" with 60 seconds duration
    Then the QR code data should follow the structured format
    And the QR code data should contain the correct event and location
    And the expiry timestamp should be correctly calculated

  @core
  Scenario: Parse QR code data
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456"
    When the QR code data is parsed
    Then the parsed data should match the original event and location
    And the parsed data should include a valid timestamp and signature

  @core
  Scenario Outline: Verify QR code validity
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456" with <duration> seconds duration
    When the QR code is verified at location "<verify_location>" after <delay> seconds
    Then the verification result should be <expected_result>

    Examples:
      | duration | verify_location | delay | expected_result |
      | 60       | locationPQR456  | 1     | True            |
      | 60       | wrong_location  | 1     | False           |
      | 60       | locationPQR456  | 70    | False           |
      | 60       | locationPQR456  | 59    | True            |

  @security
  Scenario: Detect tampered QR code signature
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456"
    And the QR code signature is tampered with
    When the QR code is verified at location "locationPQR456"
    Then the verification result should be False

  @security
  Scenario: Detect tampered QR code content
    Given a QR code is generated for event "eventXYZ789" at location "locationPQR456"
    And the QR code event ID is changed to "tampered_event"
    When the QR code is verified at location "locationPQR456"
    Then the verification result should be False

  @robustness
  Scenario: Handle malformed or empty QR data
    When an empty QR code string is verified
    Then the verification result should be False
