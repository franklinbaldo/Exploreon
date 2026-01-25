# src/qr_system.py

import time
import hashlib

class DynamicQRGenerator:
    """
    Generates and manages dynamic QR codes.
    """
    def __init__(self, secret_key: str):
        """
        Initializes the QR generator with a secret key for encoding.
        """
        self.secret_key = secret_key

    def generate_qr_code_data(self, event_id: str, location_id: str, duration_seconds: int = 60) -> tuple[str, int]:
        """
        Generates data for a time-sensitive QR code.

        Args:
            event_id: Identifier for the event.
            location_id: Identifier for the specific location.
            duration_seconds: How long the QR code should be considered valid from generation.

        Returns:
            A tuple containing the QR code data string and its calculated expiry timestamp.
        """
        current_timestamp = int(time.time())
        expiry_timestamp = current_timestamp + duration_seconds

        # Data to be signed: event_id, location_id (from QR), timestamp (from QR), and secret_key
        payload_to_sign = f"{event_id}|{location_id}|{current_timestamp}|{self.secret_key}"
        signature = hashlib.sha256(payload_to_sign.encode()).hexdigest()[:16] # Use first 16 chars of hash as signature

        # QR code content string using simple, distinct field prefixes
        # E: Event ID, LID: Location ID (of QR Issuance), TS: Timestamp of Generation, S: Signature
        qr_data_string = f"E:{event_id}|LID:{location_id}|TS:{current_timestamp}|S:{signature}"

        return qr_data_string, expiry_timestamp

    def parse_qr_code_data(self, qr_data_string: str) -> dict | None:
        """Parses a QR code data string into its component fields.

        Args:
            qr_data_string: The raw string embedded in the QR code.

        Returns:
            Dictionary with keys ``event_id``, ``location_id``, ``timestamp`` and
            ``signature`` if parsing succeeds, otherwise ``None`` when the
            string is malformed.
        """
        try:
            parts = {}
            for item in qr_data_string.split("|"):
                if ":" not in item:
                    return None
                key, value = item.split(":", 1)
                parts[key] = value

            if not {"E", "LID", "TS", "S"}.issubset(parts.keys()):
                return None

            timestamp = int(parts["TS"])

            return {
                "event_id": parts["E"],
                "location_id": parts["LID"],
                "timestamp": timestamp,
                "signature": parts["S"],
            }
        except Exception:
            return None

    def verify_qr_code_data(self, qr_data_string: str, current_location_id_for_verification: str, current_time_for_verification: int, validity_window_seconds: int = 300) -> bool:
        """
        Verifies the dynamic QR code data.
        Checks signature, timestamp (freshness), and location.

        Args:
            qr_data_string: The string data obtained from scanning the QR code.
            current_location_id_for_verification: The current location ID where verification is happening.
            current_time_for_verification: The current timestamp to check against QR's generation time.
            validity_window_seconds: How long the QR code is considered valid after its generation timestamp (TS).

        Returns:
            True if the QR code is valid, False otherwise.
        """
        try:
            parts = {}
            for item in qr_data_string.split('|'):
                # Ensure item has a colon before splitting to avoid errors on malformed data
                if ':' not in item:
                    return False # Malformed item
                key, value = item.split(':', 1)
                parts[key] = value

            event_id_from_qr = parts.get("E")
            location_id_from_qr = parts.get("LID")
            timestamp_str_from_qr = parts.get("TS")
            signature_from_qr = parts.get("S")

            if not all([event_id_from_qr, location_id_from_qr, timestamp_str_from_qr, signature_from_qr]):
                return False # Incomplete QR data

            timestamp_from_qr = int(timestamp_str_from_qr)

            # 1. Verify location: Check if the QR's embedded location matches the current verification location.
            if location_id_from_qr != current_location_id_for_verification:
                return False # Location mismatch

            # 2. Verify signature: Reconstruct the payload that would have been signed and check the signature.
            expected_payload_to_sign = f"{event_id_from_qr}|{location_id_from_qr}|{timestamp_from_qr}|{self.secret_key}"
            expected_signature = hashlib.sha256(expected_payload_to_sign.encode()).hexdigest()[:16]

            if signature_from_qr != expected_signature:
                return False # Signature mismatch

            # 3. Verify timestamp (freshness): Check if current time is within the allowed window from QR generation time.
            if current_time_for_verification > timestamp_from_qr + validity_window_seconds:
                 return False # QR code expired (passed its validity window from generation)

            return True # All checks passed

        except (ValueError, TypeError): # Catches errors from int() conversion or if parts.get() is None for critical fields
            return False # Malformed data (e.g., timestamp not an int)
        except Exception: # Catch any other unexpected errors during parsing/verification
            return False
