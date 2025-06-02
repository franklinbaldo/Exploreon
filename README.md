# Exploreon - Proof of Experience Platform

Exploreon is an experience verification platform that uses World ID biometric verification, dynamic QR codes, and semi-fungible tokens (SFTs) to prove authentic human presence at events and locations. Exploreon leverages World ID, a core component of the broader World project (which also includes the World App and WLD token), to ensure authentic human presence. Users can collect and showcase digital proof of their real-world experiences.

## Core Features
- **Biometric Verification via World ID:** Utilizes World ID, a privacy-preserving digital identity solution, to allow users to prove their unique humanity online without revealing sensitive personal data. This is achieved through a cryptographic proof of personhood, enhancing the authenticity of experience claims.
- Dynamic QR codes for on-site check-in.
- ERC-1155 Semi-Fungible Tokens (SFTs) as digital collectibles representing experiences.
- A platform for users to manage and showcase their verified experiences.

## Technology Stack (Anticipated)
- **Blockchain:** Ethereum Virtual Machine (EVM) compatible chain for SFTs (ERC-1155).
- **Identity Verification:** World ID SDK.
- **Frontend:** Mobile application (React Native anticipated, but subject to detailed design) for user interaction and QR scanning.
- **Backend:** Services for QR code management, SFT minting, user profiles, and API communication (e.g., Node.js, Python, Go - specific stack to be determined).
- **Database:** For storing user data, experience details, and off-chain metadata (e.g., PostgreSQL, MongoDB).

## Project Documentation
- **Project Initiation Document (`PID.md`):** Contains the detailed vision, objectives, scope, and initial planning for Exploreon. See [PID.md](PID.md).
- **Task List & Roadmap (`TODO.md`):** Contains a detailed breakdown of development tasks, phases, and the project roadmap. See [TODO.md](TODO.md).

## Getting Started (High-Level Overview)
Detailed setup and development steps will be outlined in `TODO.md` as the project progresses. The initial phases will involve:
1. Setting up the blockchain environment and deploying SFT contracts.
2. Integrating World ID for biometric verification.
3. Developing the dynamic QR code generation and validation system.
4. Building the mobile application frontend.
5. Developing backend services to tie these components together.

## Contributing
Details on contributing to the project will be added later. For now, refer to the `PID.md` and `TODO.md` for project direction.

```
