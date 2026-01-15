Feature: Dynamic QR Code Verification
  As a user at an event
  I want to verify my presence by scanning a dynamic QR code
  So that I can get a digital proof of my experience

  Scenario: Successful verification of a valid QR code
    Given a QR code generator is initialized with a secret key
    And an event with ID "concert_abc" is happening at location "venue_entrance_1"
    When a dynamic QR code is generated for the event and location
    And the user presents the QR code for verification at the correct location within the validity period
    Then the QR code should be successfully verified
