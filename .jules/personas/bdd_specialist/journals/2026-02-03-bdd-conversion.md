# BDD Conversion Journal - 2026-02-03

## Task: Convert legacy unit tests to BDD using pytest-bdd

### Progress
- Initialized BDD directory structure: `tests/features/`, `tests/step_defs/`.
- Plan established and approved.

### Planned Features
1. `qr_system.feature`: Covering dynamic QR code generation, parsing, and multi-factor verification.
2. `world_id_integration.feature`: Covering biometric data processing, ZKP generation, and SDK interactions.

### Notes
- Will use declarative Gherkin style.
- Shared fixtures like `secret_key` will be moved to `conftest.py`.
- Legacy `unittest` files will be removed after BDD verification.
