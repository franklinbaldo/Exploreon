# Exploreon - Decision Log

This document records key technical and strategic decisions made throughout the Exploreon project lifecycle. Its purpose is to provide clarity and context for these choices to all team members and stakeholders.

Each decision will be documented with:
- **Date:** When the decision was made.
- **Context:** The situation or problem that necessitated the decision.
- **Decision:** The choice that was made.
- **Reasoning:** Why this choice was made over alternatives.
- **Impact/Consequences:** (Optional) Any foreseen impact on the project.

---

## Decision: Choice of Blockchain Platform

- **Date:** 2025-05-31
- **Context:** The Exploreon platform requires a blockchain for minting and managing Semi-Fungible Tokens (SFTs - ERC-1155 standard). Key considerations include transaction speed, cost, developer ecosystem maturity, and user accessibility. Options mentioned in `TODO.md` included Polygon, Arbitrum, and Optimism.
- **Decision:** **Polygon PoS** is selected as the initial blockchain platform for Exploreon SFTs.
- **Reasoning:**
    - **Low Transaction Fees:** Polygon PoS offers significantly lower gas fees compared to Ethereum mainnet, making the minting and transfer of SFTs more cost-effective for users and the platform.
    - **Fast Confirmation Times:** Faster block times lead to a better user experience.
    - **Mature Ecosystem & Developer Support:** Polygon has a well-established ecosystem with extensive developer tools (Hardhat, Foundry support), documentation, and a large community. This facilitates faster development and easier integration.
    - **EVM Compatibility:** Full EVM compatibility allows for the use of standard Ethereum development tools and smart contract languages (Solidity, Vyper).
    - **Growing Adoption & Liquidity:** Polygon has strong adoption, good wallet support (MetaMask, Trust Wallet, etc.), and established bridges to Ethereum, which can be beneficial for future interoperability or user asset management.
    - **Scalability Roadmap:** Polygon is actively developing further scaling solutions (e.g., Polygon zkEVM), offering potential future paths for increased scalability if needed.
- **Impact/Consequences:**
    - Development will proceed using Polygon PoS testnets (e.g., Mumbai) and mainnet.
    - Smart contracts will be written in Solidity and deployed on Polygon.
    - Users will need a Polygon-compatible wallet and MATIC tokens for gas fees (though the platform might explore gasless transactions for users in the future).
    - **World Chain Context:** While Exploreon's initial blockchain target is Polygon PoS, the team acknowledges the existence and philosophy of World Chain (an L2 designed for 'real humans'). Future integrations or strategic shifts might consider World Chain if its ecosystem and features align with Exploreon's long-term goals, particularly if deeper integration with the World App user base is desired.

---

## Guidance: Setting Up Development Environments

- **Date:** 2025-05-31
- **Context:** To ensure consistency and smooth onboarding for developers, this section outlines the recommended tools and components for setting up local development environments for Exploreon.
- **Decision:** The following tools and configurations are recommended for each part of the project:

### 1. Blockchain Development (Polygon PoS)
- **Smart Contract Language:** Solidity (latest stable version, e.g., ^0.8.0).
- **Development Framework:**
    - **Recommendation:** **Hardhat**. It offers a flexible environment for compiling, deploying, testing, and debugging Ethereum software.
    - **Alternatives:** Foundry (Rust-based, known for speed and efficiency) can be considered by developers comfortable with it.
- **Local Blockchain:** Hardhat Network (comes with Hardhat).
- **Wallet:** MetaMask browser extension (configured for Polygon Mainnet and Mumbai Testnet).
- **Node Provider RPC URL:** An Alchemy or Infura account is recommended for reliable access to Polygon nodes (Mumbai for testing, Mainnet for deployment).
- **PolygonScan API Key:** For verifying contracts and interacting with PolygonScan APIs.

### 2. Backend Development
- **Programming Language & Runtime:** **Node.js** (LTS version, e.g., v18.x or v20.x).
- **Package Manager:** **npm** (comes with Node.js) or **Yarn Classic/Berry**.
- **Web Framework:** **Express.js**. It's a minimal and flexible Node.js web application framework, well-suited for building robust APIs.
- **Database (Initial Choice):** **PostgreSQL**. A powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.
    - **ORM/Query Builder:** Prisma or Knex.js (to be decided during initial backend setup).
- **API Testing Tool:** Postman, Insomnia, or VS Code REST Client.

### 3. Frontend Development (Mobile - React Native)
- **Core Framework:** **React Native**.
- **Language:** JavaScript or TypeScript (TypeScript is highly recommended for larger projects and will be assumed).
- **Node.js & Watchman:** Required by React Native. Install Node.js (LTS version) and Watchman (especially for macOS users).
- **React Native CLI:** Use the built-in React Native CLI.
- **iOS Development:**
    - macOS computer.
    - Xcode (latest version from Mac App Store).
    - CocoaPods (dependency manager for Xcode).
- **Android Development:**
    - Android Studio (latest version).
    - Java Development Kit (JDK) - Android Studio usually bundles its own.
    - Android SDK and build tools (manageable via Android Studio).
- **Package Manager:** npm or Yarn.
- **State Management:** Redux Toolkit (recommended for scalable state management) or Zustand/Context API for simpler needs.
- **Navigation:** React Navigation.

### 4. General Tools
- **Version Control:** **Git** & a Git hosting service (e.g., GitHub, GitLab).
- **IDE:** **Visual Studio Code (VS Code)** is highly recommended due to its excellent support for JavaScript/TypeScript, Solidity, and various extensions.
- **Code Formatting:** Prettier (integrated into IDE).
- **Linting:** ESLint (configured for TypeScript, React, Node.js).
- **Communication:** Slack, Discord, or Microsoft Teams (to be decided by team).

- **Reasoning:** These choices represent a modern, widely adopted, and well-supported stack for building full-stack applications involving blockchain, backend APIs, and mobile frontends. They offer good developer experience and community support.
- **Impact/Consequences:** Developers will need to install and configure these tools on their local machines. Project setup scripts or Docker configurations might be considered later to streamline environment setup.

---

## Guidance: Git Repository Structure & Branching Strategy

- **Date:** 2025-05-31
- **Context:** A clear Git repository structure and branching strategy are essential for collaborative development, managing releases, and maintaining code quality.
- **Decision:** The following structure and strategy will be adopted for the Exploreon project:

### 1. Directory Structure (Monorepo Approach)
A monorepo structure is chosen to keep all project code (blockchain, backend, frontend, docs) in a single Git repository. This simplifies dependency management (e.g., shared types between frontend/backend) and coordinated changes.

```
exploreon/
├── blockchain/         # Smart contracts (Hardhat/Foundry project)
│   ├── contracts/
│   ├── scripts/
│   ├── test/
│   └── hardhat.config.js (or foundry.toml)
├── backend/            # Backend services (Node.js/Express project)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── ...
├── frontend/           # React Native mobile application
│   ├── src/
│   ├── ios/
│   ├── android/
│   ├── package.json
│   └── ...
├── docs/               # Project documentation
│   ├── PID.md
│   ├── TODO.md
│   ├── DECISIONS.md
│   └── (other architectural diagrams, guides, etc.)
├── packages/           # Optional: For shared libraries/utilities (e.g., common types)
│   └── common-types/
│       ├── src/
│       └── package.json
├── .gitignore
├── README.md           # Main project README
└── ... (CI/CD configs, global prettier/eslint configs)
```

### 2. Branching Strategy (GitFlow Variation)

A variation of the GitFlow branching model is recommended:

- **`main`:** This branch represents the latest production-ready code. It should always be stable and deployable. Direct commits to `main` are forbidden. Merges to `main` should only come from `release` branches or hotfix branches.
- **`develop`:** This is the primary integration branch for ongoing development. All feature branches are merged into `develop` after code review and passing tests. Nightly builds or CI builds can be run from `develop`.
- **Feature Branches (`feature/<feature-name>` or `feat/<feature-name>`):**
    - Branched from `develop`.
    - Used for developing new features (e.g., `feature/user-profile`, `feat/qr-code-scanning`).
    - Merged back into `develop` via Pull Requests (PRs) with code review.
    - Should be short-lived.
- **Bugfix Branches (`bugfix/<issue-id>` or `fix/<issue-id>`):**
    - Branched from `develop` for fixing non-critical bugs.
    - Merged back into `develop` via PRs.
- **Release Branches (`release/<version>`):**
    - Branched from `develop` when `develop` has reached a stable point and is ready for a new production release (e.g., `release/v1.0.0`).
    - Used for final testing, bug fixing, and preparing for deployment (version bumping, documentation updates).
    - Once ready, `release/<version>` is merged into `main` (and tagged) and also back into `develop` (to ensure fixes from the release branch are incorporated into future development).
- **Hotfix Branches (`hotfix/<issue-id>` or `hotfix/<version>`):**
    - Branched from `main` to address critical bugs in production that need immediate fixing.
    - Once the fix is complete and tested, it's merged back into `main` (and tagged with a patch version, e.g., `v1.0.1`) AND into `develop` (or the current `release` branch if one is active) to ensure the fix is not lost.

### 3. Commit Messages
- Conventional Commits specification is recommended for clear and automated changelog generation. Example: `feat: add user authentication endpoint`.

- **Reasoning:**
    - The monorepo simplifies cross-component work and dependency management.
    - The GitFlow variation provides a robust framework for managing development, releases, and hotfixes, ensuring stability in `main` while allowing agile development in feature branches.
    - Conventional Commits improve readability of Git history and can automate versioning and changelog generation.
- **Impact/Consequences:**
    - Developers need to adhere to the branching strategy and commit message conventions.
    - CI/CD pipelines will be configured based on this branching model (e.g., deployments from `main`, builds from `develop`).

---

## Major Decision: World ID Integration Strategy

- **Date:** 2025-06-03 (Placeholder, adjust as needed)
- **Context:** Effective and secure integration with World ID is crucial for the "proof of presence" and Sybil resistance features of Exploreon. This section outlines the core strategies for this integration.
- **Decision/Guidance:**
    - **Backend Verification of Proofs:** All World ID proofs presented by users for experience verification *must* be verified through a secure backend call to the World ID service (`/api/v2/verify/{app_id}` or GraphQL endpoint). Frontend verification alone is insufficient due to security risks.
    - **Use of "Actions":** Exploreon will define specific 'Actions' in the World ID Developer Portal for each distinct experience or type of verification (e.g., 'exploreon-concert-checkin-event123', 'exploreon-location-visit-poi456'). These actions will be used in the `Verify` command.
    - **Nullifier Hash Management:** The backend must correctly handle `nullifier_hash` values returned from successful World ID verifications. This hash, unique per user per action, is the primary mechanism to prevent a single user from verifying the same unique experience multiple times.
    - **Choice of Verification Level:** Exploreon will primarily target `VerificationLevel.Orb` for its experiences to ensure the highest level of Sybil resistance. The specific level may be configurable per experience type in the future if deemed necessary. This will be requested in the `Verify` command.
    - **Developer Portal Usage:** The World ID Developer Portal is the central point for managing Exploreon's application settings, credentials (Client ID, Secret, API Keys), and defining/managing 'Actions'. All sensitive credentials must be stored securely and accessed only by the backend.
    - **API Key Security for Backend:** API keys obtained from the World ID Developer Portal for backend verification must be treated as highly sensitive secrets, stored securely (e.g., environment variables, secret manager), and only used for server-to-server communication via `Authorization: Bearer $API_KEY` header.
- **Reasoning:** These strategies prioritize security, prevent abuse (e.g., multiple claims by the same person for a unique event), and align with World ID best practices for robust integration. Using distinct actions provides granularity and better control over verification contexts.
- **Impact/Consequences:**
    - Backend development must include logic for World ID proof verification and nullifier hash management.
    - Secure storage mechanisms for API keys and other credentials are required.
    - The setup and management of the World ID Developer Portal will be an ongoing administrative task.

---

## Guidance: Data Privacy and Consent for World ID

- **Date:** 2025-06-03 (Placeholder, adjust as needed)
- **Context:** Ensuring user privacy and obtaining informed consent are paramount when integrating biometric verification systems like World ID.
- **Decision/Guidance:**
    - **Data Minimization:** When integrating with World ID, Exploreon will request only the minimum necessary information/scope required for its functionality (i.e., proof of personhood for a specific action).
    - **User Consent:** Clear user consent must be obtained before initiating any World ID verification process. Users should be informed about what is being verified and why.
- **Reasoning:** Adherence to data privacy principles builds user trust and ensures compliance with potential regulatory requirements.
- **Impact/Consequences:**
    - Frontend UI/UX must include clear consent flows before World ID interaction.
    - Backend systems must be designed to handle only the necessary data from World ID.

---

## Initial Data Models (Draft)

- **Date:** 2025-05-31
- **Context:** To facilitate backend development and ensure a common understanding of data structures, initial drafts of core data models are required. These are based on the Exploreon project's requirements for user management, experience tracking, SFT representation, and verification processes.
- **Decision:** The following structures are proposed as initial drafts. These will likely evolve as development progresses.

### 1. User Model
Represents an end-user of the Exploreon platform.

```json
{
  "userId": "UUID", // Primary Key
  "walletAddress": "string", // User's primary blockchain wallet address (e.g., Polygon address)
  "worldId": "string", // Unique identifier from World ID verification (if applicable, store securely)
  "username": "string", // Optional, user-chosen display name
  "email": "string", // Optional, for communication
  "profileImageUrl": "string", // Optional
  "collectedSfts": [ // Array of SFT IDs or references
    {
      "sftId": "UUID",
      "acquiredAt": "timestamp"
    }
  ],
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### 2. Experience Model
Represents an event, activity, or location that can be verified.

```json
{
  "experienceId": "UUID", // Primary Key
  "name": "string", // e.g., "Coachella 2024 - Weekend 1", "Mount Everest Summit Climb"
  "description": "text",
  "imageUrl": "string",
  "location": {
    "name": "string", // e.g., "Empire Polo Club", "Mount Everest"
    "latitude": "float", // Optional
    "longitude": "float" // Optional
  },
  "startTime": "timestamp",
  "endTime": "timestamp",
  "organizer": "string", // Name or ID of the event organizer/partner
  "tags": ["string"], // e.g., ["music", "festival", "adventure", "climbing"]
  "sftContractAddress": "string", // Address of the SFT contract for this experience
  "maxVerifications": "integer", // Optional: if there's a limit
  "isActive": "boolean", // Whether this experience is currently verifiable
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### 3. SFT (Semi-Fungible Token) Model
Represents the digital collectible (ERC-1155 token) a user receives as proof of experience. This model describes the off-chain metadata associated with an SFT. The on-chain SFT will have a unique token ID.

```json
{
  "sftId": "UUID", // Primary Key for off-chain metadata record
  "experienceId": "UUID", // Foreign Key linking to the Experience
  "tokenId": "BigInt", // The unique ID of the token within the ERC-1155 contract
  "ownerWalletAddress": "string", // Current owner's wallet address (can be updated via blockchain events)
  "metadata": { // ERC-1155 Metadata JSON structure
    "name": "string", // e.g., "Proof of Attendance: Coachella 2024 - Weekend 1"
    "description": "string", // Detailed description of what this SFT represents
    "image": "URL", // URL to the SFT image (e.g., IPFS link)
    "attributes": [
      { "trait_type": "Experience", "value": "Coachella 2024 - Weekend 1" },
      { "trait_type": "Date", "value": "2024-04-12" },
      { "trait_type": "Location", "value": "Empire Polo Club" },
      { "trait_type": "VerificationMethod", "value": "WorldID + DynamicQR" }
      // Other relevant traits
    ]
  },
  "mintedAt": "timestamp",
  "transactionHash": "string" // Transaction hash of the mint operation
}
```

### 4. Verification Attempt Model
Records each attempt by a user to verify presence at an experience.

```json
{
  "verificationId": "UUID", // Primary Key
  "userId": "UUID", // Foreign Key linking to User
  "experienceId": "UUID", // Foreign Key linking to Experience
  "attemptTimestamp": "timestamp",
  "status": "string", // e.g., "pending", "successful", "failed_qr", "failed_worldid", "already_verified"
  "qrCodeData": "string", // Data scanned from the QR code
  "worldIdVerificationProof": "json", // Proof object from World ID, if successful
  "deviceInfo": "json", // Optional: Info about the device used for verification
  "sftMintedId": "UUID", // Foreign Key to SFT record, if minting was successful
  "failureReason": "string", // Optional: If status is 'failed'
  "createdAt": "timestamp"
}
```

- **Reasoning:** These models provide a starting point for database design and API development. They aim to capture the essential information needed for Exploreon's core functionality. The use of UUIDs allows for globally unique identifiers. Timestamps help in auditing and tracking.
- **Impact/Consequences:** Backend developers can use these models to start designing database schemas and API endpoints. Frontend developers can understand the data they will be interacting with. These models will be refined during the development of specific features.

---
```
