Feature: SFT Minting for Experience Verification
  As a user of the Exploreon platform
  I want to mint a Semi-Fungible Token (SFT) after a successful experience verification
  So that I have a digital proof of my attendance.

  Scenario: Successful SFT Minting for a Verified Experience
    Given a user has a successful experience verification for a specific event and location
    When the system processes the verification for SFT minting
    Then a new SFT with correct metadata should be minted for the user's account

  Scenario: Attempting to Mint an SFT with an Invalid Verification
    Given a user has an unsuccessful or invalid experience verification
    When the system attempts to process the verification for SFT minting
    Then no SFT should be minted and an error should be logged

  Scenario: Attempting to Mint a Duplicate SFT for the Same Experience
    Given a user has already minted an SFT for a specific experience
    When the system processes another verification for the same experience
    Then no duplicate SFT should be minted and the system should recognize the duplicate
