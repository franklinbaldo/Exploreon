Feature: World ID Integration
  As a system integrator
  I want to verify users using World ID biometric data
  So that I can ensure unique human presence.

  Background:
    Given the World ID SDK is initialized with app ID "test_app_123" and action ID "test_action_abc"

  Scenario: Verifying a user with a valid signal
    When a user provides a valid signal "valid_signal"
    Then the user should be successfully verified

  Scenario: Failing to verify a user with an empty signal
    When a user provides an empty signal
    Then the user verification should fail

  Scenario: Processing biometric data
    When raw biometric data "test_biometric_data" is processed
    Then the processed data should indicate success
    And it should contain a data hash

  Scenario: Generating a zero-knowledge proof
    Given raw biometric data "test_biometric_data" is processed
    When a zero-knowledge proof is generated
    Then the proof should start with "zkp_"
    And it should contain the data hash

  Scenario: Handling successful verification result
    When a successful verification result is handled with proof "sample_proof_123"
    Then the status should be "success"
    And the result should contain the proof "sample_proof_123"

  Scenario: Handling failed verification result
    When a failed verification result is handled
    Then the status should be "failure"
    And the result should not contain a proof
