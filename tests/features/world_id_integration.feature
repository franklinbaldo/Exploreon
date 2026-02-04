Feature: World ID Integration
  As a user
  I want to verify my humanity using World ID
  So that I can securely participate in events

  Scenario: Verify a user with World ID
    Given a World ID SDK initialized with app ID "test_app_123" and action ID "test_action_abc"
    When the user is verified with signal "valid_signal"
    Then the verification status should be successful

  Scenario: User verification fails with empty signal
    Given a World ID SDK initialized with app ID "test_app_123" and action ID "test_action_abc"
    When the user is verified with signal ""
    Then the verification status should be failure

  Scenario: Process biometric data
    When biometric data "test_biometric_data" is processed
    Then the processed data should indicate success and include a data hash

  Scenario: Generate zero-knowledge proof
    Given processed biometric data from "test_biometric_data"
    When a zero-knowledge proof is generated
    Then the proof should be valid and contain the data hash

  Scenario: Handle successful verification result
    When a successful verification result is handled with proof "sample_proof_123"
    Then the result status should be "success"
    And the result should contain the proof "sample_proof_123"

  Scenario: Handle failed verification result
    When a failed verification result is handled
    Then the result status should be "failure"
    And the result should not contain a proof
