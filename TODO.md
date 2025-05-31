# Exploreon - Project TODO List

This document outlines the development tasks and phases for the Exploreon platform.
Refer to `PID.md` for the overall project vision, scope, and objectives.

## Phase 1: Foundation (Target: Months 1-2)

- [ ] **Project Setup & Planning:**
    - [ ] Finalize choice of specific blockchain (e.g., Polygon, Arbitrum, Optimism) for ERC-1155 SFTs.
    - [ ] Set up development environments for blockchain, backend, and frontend.
    - [ ] Initialize Git repository with main branches (main, develop).
    - [ ] Define detailed data models for Users, Experiences, SFTs, Verifications.
    - [ ] Establish CI/CD pipeline basics (e.g., GitHub Actions for linting, basic tests).
- [ ] **World ID Integration - Initial Setup:**
    - [ ] Sign up for World ID developer access.
    - [ ] Integrate World ID SDK into a prototype application/environment.
    - [ ] Test basic biometric verification flow (proof of personhood).
    - [ ] Research secure handling of World ID verification results.
- [ ] **Dynamic QR System - Core Logic:**
    - [ ] Design QR code payload structure (e.g., event ID, timestamp, location hints).
    - [ ] Develop backend logic for generating time-sensitive, single-use QR codes.
    - [ ] Develop initial QR code scanning and validation mechanism for a prototype.
- [ ] **Smart Contract Development - SFT Basics:**
    - [ ] Develop ERC-1155 SFT contract.
        - [ ] Define SFT metadata structure (experience name, date, location, unique ID).
        - [ ] Implement basic minting function (callable by authorized backend).
        - [ ] Implement basic transfer/ownership functions.
    - [ ] Deploy initial SFT contract to a testnet.
    - [ ] Write basic unit tests for SFT contract.
- [ ] **Backend Services - Initial Stubbing:**
    - [ ] Set up basic backend project (e.g., Node.js/Express, Python/FastAPI).
    - [ ] Define initial API endpoints for:
        - QR code generation.
        - Verification submission (World ID result + QR data).
        - SFT minting request.
    - [ ] Stub out these API endpoints with mock responses.

## Phase 2: Core Features (Target: Months 3-4)

- [ ] **Verification Flow - End-to-End:**
    - [ ] Frontend: Implement UI for QR code scanning.
    - [ ] Frontend: Implement UI for initiating World ID verification.
    - [ ] Backend: Process verification requests (validate QR, World ID result).
    - [ ] Backend: Trigger SFT minting upon successful verification.
    - [ ] Frontend: Display confirmation of successful verification and SFT receipt.
- [ ] **SFT Implementation - Full Features:**
    - [ ] Finalize SFT metadata standard for Exploreon experiences.
    - [ ] Implement batch minting capabilities in the SFT contract.
    - [ ] Backend: System for managing experience details and corresponding SFT metadata.
    - [ ] Frontend: UI for users to view their collected SFTs (basic wallet view).
- [ ] **Experience Tracking System - Backend:**
    - [ ] Database schema for storing created experiences (name, description, location, date, associated SFT IDs).
    - [ ] API endpoints for CRUD operations on experiences (admin/partner facing).
    - [ ] System for linking verified attendance to specific experiences and users.
- [ ] **User Profiles - Basic:**
    - [ ] Backend: User authentication and profile management (e.g., link to wallet address).
    - [ ] Database schema for basic user profiles.
    - [ ] Frontend: Basic user profile screen displaying collected SFTs.
- [ ] **Security Hardening - Initial Pass:**
    - [ ] Review and secure API endpoints (authentication, authorization).
    - [ ] Protect against common vulnerabilities (e.g., replay attacks on QR codes).

## Phase 3: Enhancement (Target: Months 5-6)

- [ ] **Social Features:**
    - [ ] Frontend: Allow users to share their verified experiences/SFTs on social media.
    - [ ] Backend: Generate shareable links/images for experiences.
    - [ ] (Optional) Basic commenting or reactions on experiences within the platform.
- [ ] **Partner Integration - Proof of Concept:**
    - [ ] Develop a portal or API for event partners to create/manage experiences.
    - [ ] Develop a system for partners to issue/display dynamic QR codes at their venues.
    - [ ] Test partner integration with 1-2 pilot partners.
- [ ] **Community Tools - Basic:**
    - [ ] Simple in-app feed of recently verified experiences (public or user-specific).
    - [ ] Links to community channels (e.g., Discord, Telegram).
- [ ] **Frontend Polish & UX Improvements:**
    - [ ] Refine UI based on initial user testing.
    - [ ] Improve navigation and user flows.
    - [ ] Add animations and transitions for a smoother experience.
- [ ] **Testing - Comprehensive:**
    - [ ] Write integration tests for key user flows.
    - [ ] Conduct usability testing sessions.
    - [ ] Perform security testing and vulnerability scanning.

## Phase 4: Launch (Target: Month 7)

- [ ] **Public Beta Program:**
    - [ ] Recruit beta testers.
    - [ ] Deploy application to a staging environment accessible to beta testers.
    - [ ] Collect feedback and bug reports.
- [ ] **Initial Events Onboarding:**
    - [ ] Onboard a selection of initial events/partners for the public launch.
    - [ ] Ensure their experiences are correctly set up in the system.
- [ ] **Marketing & Community Building:**
    - [ ] Prepare launch marketing materials.
    - [ ] Engage with target communities.
- [ ] **App Store / Platform Preparation:**
    - [ ] Prepare app store listings (if a mobile app is the primary frontend).
    - [ ] Ensure website is ready for public access.
- [ ] **Final Security Audits:**
    - [ ] Conduct external security audit of smart contracts.
    - [ ] Conduct penetration testing of the platform.
- [ ] **Go-Live Deployment:**
    - [ ] Deploy backend to production environment.
    - [ ] Deploy smart contracts to mainnet.
    - [ ] Make frontend accessible to the public.

## Post-Launch & Ongoing

- [ ] **Monitoring & Support:**
    - [ ] Set up comprehensive logging and monitoring for all systems.
    - [ ] Establish customer support channels.
- [ ] **Iterate Based on Feedback:**
    - [ ] Collect user feedback and analytics.
    - [ ] Prioritize and plan V2 features and improvements.
- [ ] **Scale & Optimize:**
    - [ ] Monitor system performance and scale infrastructure as needed.
    - [ ] Optimize costly operations.
- [ ] **Legal & Compliance Review:**
    - [ ] Continuously review and update privacy policies and terms of service.
- [ ] **Partnership Expansion:**
    - [ ] Actively seek and onboard new event and technology partners.

```
