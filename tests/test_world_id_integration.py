# tests/test_world_id_integration.py

import unittest
from src.world_id_integration import (
    WorldIDSDK,
    process_biometric_data,
    generate_zero_knowledge_proof,
    handle_verification_result
)

class TestWorldIDIntegration(unittest.TestCase):

    def setUp(self):
        self.app_id = "test_app_123"
        self.action_id = "test_action_abc"
        self.sdk = WorldIDSDK(app_id=self.app_id, action_id=self.action_id)
        self.sample_data = b"test_biometric_data"
        self.processed_data_sample = {"processed": True, "data_hash": hash(self.sample_data)}

    def test_world_id_sdk_init(self):
        self.assertEqual(self.sdk.app_id, self.app_id)
        self.assertEqual(self.sdk.action_id, self.action_id)

    def test_world_id_sdk_verify_user(self):
        self.assertTrue(self.sdk.verify_user("valid_signal"))
        self.assertFalse(self.sdk.verify_user(""))

    def test_process_biometric_data(self):
        result = process_biometric_data(self.sample_data)
        self.assertTrue(result["processed"])
        self.assertIn("data_hash", result)
        self.assertEqual(result["data_hash"], hash(self.sample_data))

    def test_generate_zero_knowledge_proof(self):
        proof = generate_zero_knowledge_proof(self.processed_data_sample)
        self.assertTrue(proof.startswith("zkp_"))
        self.assertIn(str(self.processed_data_sample["data_hash"]), proof)

    def test_handle_verification_result_success(self):
        result = handle_verification_result(True, "sample_proof_123")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["proof"], "sample_proof_123")
        self.assertIn("success", result["message"].lower())

    def test_handle_verification_result_failure(self):
        result = handle_verification_result(False, "")
        self.assertEqual(result["status"], "failure")
        self.assertIsNone(result["proof"])
        self.assertIn("failed", result["message"].lower())

if __name__ == '__main__':
    unittest.main()
