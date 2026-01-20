# src/sft_system.py

class SFTManager:
    """
    Manages the creation of Semi-Fungible Tokens (SFTs).
    """
    def __init__(self, contract_address: str):
        self.contract_address = contract_address
        self.sfts = []

    def create_sfts(self, total_supply: int):
        """
        Creates a specified number of SFTs for the event.
        """
        if not self.contract_address:
            raise ValueError("A valid event contract must be set.")

        for i in range(total_supply):
            sft = {
                "id": i + 1,
                "contract": self.contract_address
            }
            self.sfts.append(sft)

        return self.sfts
