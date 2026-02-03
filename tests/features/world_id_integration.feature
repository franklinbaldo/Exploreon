Feature: World ID Integration
  As a developer
  I want to integrate World ID biometric verification
  So that I can verify users' unique humanity in a privacy-preserving manner

  @core
  Scenario: Initialize World ID SDK
    Given an app ID "test_app_123" and an action ID "test_action_abc"
    When the World ID SDK is initialized
    Then the SDK should have the correct app ID and action ID

  @core
  Scenario: Verify a user with a signal
    Given the World ID SDK is initialized with app ID "test_app_123" and action ID "test_action_abc"
    When a user is verified with signal "valid_signal"
    Then the verification status should be True
    When a user is verified with an empty signal
    Then the verification status should be False

  @biometric
  Scenario: Process biometric data
    When raw biometric data "test_biometric_data" is processed
    Then the processed data should indicate success
    And the processed data should contain a hash of the raw data

  @crypto
  Scenario: Generate Zero-Knowledge Proof
    Given raw biometric data "test_biometric_data" has been processed
    When a zero-knowledge proof is generated
    Then the proof should start with "zkp_"
    And the proof should contain the data hash

  @core
  Scenario: Handle verification result
    When a successful verification is handled with proof "sample_proof_123"
    Then the final result status should be "success"
    And the result should contain the proof "sample_proof_123"
    And the result message should indicate success

  @core
  Scenario: Handle failed verification result
    When a failed verification is handled
    Then the final result status should be "failure"
    And the result should not contain a proof
    And the result message should indicate failure
