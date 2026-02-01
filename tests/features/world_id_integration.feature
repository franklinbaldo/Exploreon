Feature: World ID Integration
    As a user
    I want to verify my humanity using World ID
    So that I can securely claim my experience tokens

    @core
    Scenario: Initialize the World ID SDK
        When the World ID SDK is initialized with app ID "app_123" and action ID "action_abc"
        Then the SDK should have the correct app ID and action ID

    @core
    Scenario: Verify a user with a valid signal
        Given the World ID SDK is initialized
        When a user provides a valid signal "user_signal_123"
        Then the user verification should be successful

    @core
    Scenario: Process biometric data
        When biometric data "raw_biometric_bytes" is processed
        Then the processed data should be marked as processed
        And it should contain a hash of the original data

    @core
    Scenario: Generate a zero-knowledge proof
        Given biometric data has been processed
        When a zero-knowledge proof is generated
        Then the proof should start with "zkp_"
        And it should contain the data hash

    @core
    Scenario: Handle successful verification result
        When a successful verification result is handled with proof "proof_789"
        Then the status should be "success"
        And the result should contain the proof
        And the message should indicate success

    @core
    Scenario: Handle failed verification result
        When a failed verification result is handled
        Then the status should be "failure"
        And the result should not contain a proof
        And the message should indicate failure
