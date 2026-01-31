Feature: World ID Integration
  As a developer
  I want to integrate World ID biometric verification
  So that I can verify authentic human presence

  Scenario: Initialize World ID SDK
    Given an app ID "test_app_123" and an action ID "test_action_abc"
    When the SDK is initialized
    Then the SDK should have the correct app ID and action ID

  Scenario: Verify user with a signal
    Given an initialized World ID SDK
    When a user provides a valid signal "valid_signal"
    Then the user should be successfully verified

  Scenario: Fail user verification with empty signal
    Given an initialized World ID SDK
    When a user provides an empty signal
    Then the user verification should fail

  Scenario: Process biometric data
    When the system processes biometric data "test_biometric_data"
    Then the processed data should indicate success
    And the processed data should contain a hash of the original data

  Scenario: Generate zero-knowledge proof
    Given processed biometric data from "test_biometric_data"
    When the system generates a zero-knowledge proof
    Then the proof should start with "zkp_"
    And the proof should contain the data hash

  Scenario: Handle successful verification result
    When the system handles a successful verification with proof "sample_proof_123"
    Then the result status should be "success"
    And the result should contain the proof "sample_proof_123"
    And the result message should indicate success

  Scenario: Handle failed verification result
    When the system handles a failed verification
    Then the result status should be "failure"
    And the result should not contain a proof
    And the result message should indicate failure
