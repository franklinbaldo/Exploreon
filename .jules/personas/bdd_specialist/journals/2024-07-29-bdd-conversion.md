# BDD Conversion Journal - 2024-07-29

## Goal: Convert `test_qr_system.py` to BDD

### Progress:

- **[X] Initial Setup:** Created `tests/features` and `tests/step_defs` directories. Added `pytest-bdd` to `requirements.txt`.
- **[X] Feature Definition:** Wrote `tests/features/qr_verification.feature` to cover the core verification logic.
- **[X] Step Implementation:** Implemented step definitions in `tests/step_defs/test_qr_verification.py`.
- **[X] Refactoring:** Created `tests/step_defs/conftest.py` to house shared fixtures like `qr_generator`.
- **[X] Execution:** Ran the new BDD tests alongside the existing unit tests. All tests passed after fixing a flaky test.

### Notes:

- The initial implementation of the expired test case was flaky due to `time.sleep()`. I refactored it to be deterministic by calculating the expiry time based on the timestamp in the QR data.
- The BDD tests now provide a clear, human-readable specification of the `DynamicQRGenerator`'s behavior.
