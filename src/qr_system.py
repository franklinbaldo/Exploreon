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


# Example Usage (for demonstration purposes, if run directly)
if __name__ == '__main__':
    generator = DynamicQRGenerator(secret_key="my_super_secret_key_12345")

    event = "concert_abc"
    loc = "venue_entrance_1"
    duration = 120 # seconds

    print("\n--- Generating QR Code ---")
    qr_data, expiry_ts = generator.generate_qr_code_data(event_id=event, location_id=loc, duration_seconds=duration)
    print(f"QR Data String: {qr_data}")
    print(f"Intended Expiry Timestamp (for info): {expiry_ts}")

    # Simulate verification at different times and conditions
    current_time = int(time.time())

    print(f"\n--- Verifying QR Code (Successful Case) ---")
    # Simulate scanning immediately at the correct location
    time.sleep(1) # Small delay
    actual_current_time = int(time.time())
    is_valid_now = generator.verify_qr_code_data(
        qr_data_string=qr_data,
        current_location_id_for_verification=loc,
        current_time_for_verification=actual_current_time,
        validity_window_seconds=duration # Using the same duration for verification window
    )
    print(f"Verification Result (Correct Location, Fresh, Time: {actual_current_time}): {is_valid_now}")

    print(f"\n--- Verifying QR Code (Wrong Location) ---")
    is_valid_wrong_loc = generator.verify_qr_code_data(
        qr_data_string=qr_data,
        current_location_id_for_verification="backstage_door",
        current_time_for_verification=actual_current_time,
        validity_window_seconds=duration
    )
    print(f"Verification Result (Wrong Location, Time: {actual_current_time}): {is_valid_wrong_loc}")

    print(f"\n--- Verifying QR Code (Tampered Signature) ---")
    tampered_qr_data_sig = qr_data.replace(qr_data[qr_data.findS("S:")+2:], "tampered_sig_value") # Tamper signature part
    is_valid_tampered_sig = generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data_sig,
        current_location_id_for_verification=loc,
        current_time_for_verification=actual_current_time,
        validity_window_seconds=duration
    )
    print(f"Verification Result (Tampered Signature, Time: {actual_current_time}): {is_valid_tampered_sig}")

    print(f"\n--- Verifying QR Code (Tampered Event ID) ---")
    tampered_qr_data_event = qr_data.replace(f"E:{event}", f"E:hacked_event") # Tamper event ID part
    is_valid_tampered_event = generator.verify_qr_code_data(
        qr_data_string=tampered_qr_data_event,
        current_location_id_for_verification=loc,
        current_time_for_verification=actual_current_time,
        validity_window_seconds=duration
    )
    print(f"Verification Result (Tampered Event ID, Time: {actual_current_time}): {is_valid_tampered_event}")

    print(f"\n--- Verifying QR Code (Expired) ---")
    # Simulate time passing beyond the validity window for expiry check
    expired_time = int(time.time()) + duration + 10 # 10 seconds after it should have expired
    is_valid_expired = generator.verify_qr_code_data(
        qr_data_string=qr_data,
        current_location_id_for_verification=loc,
        current_time_for_verification=expired_time,
        validity_window_seconds=duration
    )
    print(f"Verification Result (Expired, Verification Time: {expired_time}): {is_valid_expired}")

    print(f"\n--- Verifying QR Code (Malformed QR String) ---")
    malformed_qr = "E:event|LID:loc" # Missing TS and S, and values
    is_valid_malformed = generator.verify_qr_code_data(
        qr_data_string=malformed_qr,
        current_location_id_for_verification=loc,
        current_time_for_verification=actual_current_time,
        validity_window_seconds=duration
    )
    print(f"Verification Result (Malformed QR): {is_valid_malformed}")
