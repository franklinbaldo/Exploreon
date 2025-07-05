# tests/test_qr_system.py

import unittest
import time
from src.qr_system import DynamicQRGenerator

class TestDynamicQRSystem(unittest.TestCase):

    def setUp(self):
        self.secret = "test_secret_key_for_qr_tests"
        self.generator = DynamicQRGenerator(secret_key=self.secret)
        self.event_id = "eventXYZ789"
        self.location_id = "locationPQR456"
        self.default_duration = 60 # seconds
        self.default_verify_window = 60 # seconds, align with generation duration for tests

    def test_qr_generator_init(self):
        self.assertEqual(self.generator.secret_key, self.secret)

    def test_generate_qr_code_data_structure_and_expiry(self):
        qr_data, expiry_ts = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )

        self.assertIsInstance(qr_data, str)
        self.assertIsInstance(expiry_ts, int)

        # Check for expected fields based on new structure "E:...|LID:...|TS:...|S:..."
        self.assertTrue(qr_data.startswith(f"E:{self.event_id}|LID:{self.location_id}"))
        self.assertIn(f"|TS:", qr_data)
        self.assertIn(f"|S:", qr_data)

        # Verify parts
        parts = dict(item.split(":", 1) for item in qr_data.split("|"))
        self.assertEqual(parts["E"], self.event_id)
        self.assertEqual(parts["LID"], self.location_id)
        self.assertTrue(parts["TS"].isdigit())
        self.assertTrue(len(parts["S"]) == 16) # Signature length

        current_time = int(time.time())
        # Expiry timestamp should be generation_time + duration
        # Generation time is parts["TS"]
        expected_expiry = int(parts["TS"]) + self.default_duration
        self.assertEqual(expiry_ts, expected_expiry)
        # Also check relative to current time, allowing for small execution delay
        self.assertGreaterEqual(expiry_ts, current_time + self.default_duration - 5) # Allow 5s slack
        self.assertLessEqual(expiry_ts, current_time + self.default_duration + 5)

    def test_parse_qr_code_data_valid(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        parsed = self.generator.parse_qr_code_data(qr_data)
        assert parsed is not None
        self.assertEqual(parsed["event_id"], self.event_id)
        self.assertEqual(parsed["location_id"], self.location_id)
        self.assertIsInstance(parsed["timestamp"], int)
        self.assertEqual(len(parsed["signature"]), 16)

    def test_parse_qr_code_data_malformed(self):
        parsed = self.generator.parse_qr_code_data("E:bad|no_colon")
        self.assertIsNone(parsed)


    def test_verify_qr_code_data_valid(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        time.sleep(0.01) # Ensure a slight delay so current time is not exactly generation time
        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            qr_data, self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertTrue(is_valid, "Valid QR code failed verification.")

    def test_verify_qr_code_data_invalid_location(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            qr_data, "incorrect_location_ID", current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "QR code should be invalid due to wrong location.")

    def test_verify_qr_code_data_tampered_signature(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        # Tamper signature: find "S:" and change its value
        sig_marker = "|S:"
        sig_start_index = qr_data.find(sig_marker) + len(sig_marker)
        tampered_qr_data = qr_data[:sig_start_index] + "0000000000000000" # 16 char tampered sig

        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            tampered_qr_data, self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "QR code should be invalid due to tampered signature.")

    def test_verify_qr_code_data_tampered_content_event_id(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        # Tamper event_id: find "E:" and change its value
        event_marker = f"E:{self.event_id}"
        tampered_qr_data = qr_data.replace(event_marker, "E:tampered_event_id")

        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            tampered_qr_data, self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "QR code should be invalid due to tampered event ID (signature mismatch).")

    def test_verify_qr_code_data_expired(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration # e.g., 60s
        )
        # Simulate time passing beyond the validity window
        time_of_qr_generation = int(dict(item.split(":", 1) for item in qr_data.split("|"))["TS"])
        expired_verify_time = time_of_qr_generation + self.default_verify_window + 10 # 10s after window closes

        is_valid = self.generator.verify_qr_code_data(
            qr_data, self.location_id, expired_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "Expired QR code should fail verification.")

    def test_verify_qr_code_data_just_before_expiry(self):
        qr_data, _ = self.generator.generate_qr_code_data(
            self.event_id, self.location_id, duration_seconds=self.default_duration
        )
        time_of_qr_generation = int(dict(item.split(":", 1) for item in qr_data.split("|"))["TS"])
        # Verify 1 second before the window closes
        valid_verify_time = time_of_qr_generation + self.default_verify_window -1

        is_valid = self.generator.verify_qr_code_data(
            qr_data, self.location_id, valid_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertTrue(is_valid, "QR code should be valid just before expiry.")


    def test_verify_qr_code_data_incomplete_missing_field(self):
        # Construct a QR data string missing the signature part
        timestamp = int(time.time())
        incomplete_qr = f"E:{self.event_id}|LID:{self.location_id}|TS:{timestamp}" # Missing |S:signature
        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            incomplete_qr, self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "Incomplete QR data (missing signature) should be invalid.")

    def test_verify_qr_code_data_malformed_field(self):
        # Construct a QR data string with a malformed timestamp
        timestamp = "not_an_integer"
        malformed_qr = f"E:{self.event_id}|LID:{self.location_id}|TS:{timestamp}|S:1234567890abcdef"
        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            malformed_qr, self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "Malformed QR data (bad timestamp) should be invalid.")

    def test_verify_qr_code_data_empty_string(self):
        current_verify_time = int(time.time())
        is_valid = self.generator.verify_qr_code_data(
            "", self.location_id, current_verify_time, validity_window_seconds=self.default_verify_window
        )
        self.assertFalse(is_valid, "Empty QR string should be invalid.")


if __name__ == '__main__':
    unittest.main()
