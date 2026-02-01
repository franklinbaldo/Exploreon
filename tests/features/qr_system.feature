Feature: Dynamic QR System
    As an event organizer
    I want to generate and verify dynamic QR codes
    So that I can ensure authentic human presence at specific locations

    Background:
        Given the QR system is initialized with a secret key

    @core
    Scenario: Generate a dynamic QR code
        When a QR code is generated for event "concert_123" at location "entrance_A"
        Then the QR code should contain the event ID, location ID, and a timestamp
        And the QR code should have a valid signature

    @core
    Scenario: Verify a valid QR code
        Given a QR code is generated for event "festival_001" at location "main_gate"
        When the QR code is verified at location "main_gate" within the validity window
        Then the verification should be successful

    @security
    Scenario: Fail verification for an expired QR code
        Given a QR code is generated for event "festival_001" at location "main_gate" with a short duration
        When the QR code is verified after it has expired
        Then the verification should fail

    @security
    Scenario: Fail verification for a wrong location
        Given a QR code is generated for event "festival_001" at location "main_gate"
        When the QR code is verified at location "back_gate"
        Then the verification should fail

    @security
    Scenario: Fail verification for tampered signature
        Given a QR code is generated for event "festival_001" at location "main_gate"
        And the QR code signature is tampered with
        When the QR code is verified at location "main_gate"
        Then the verification should fail

    @security
    Scenario: Fail verification for tampered event ID
        Given a QR code is generated for event "festival_001" at location "main_gate"
        And the QR code event ID is changed to "fake_event"
        When the QR code is verified at location "main_gate"
        Then the verification should fail

    @robustness
    Scenario: Fail verification for malformed data
        When a malformed QR string "invalid_data" is verified at location "any_location"
        Then the verification should fail
