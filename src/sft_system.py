class SFTManager:
    """Manages the creation and tracking of Semi-Fungible Token (SFT) collections."""

    def __init__(self):
        """Initializes the SFTManager with an empty dictionary to store collections."""
        self._collections = {}

    def create_sft_collection(self, name: str, supply: int):
        """
        Creates a new SFT collection for an event.

        Args:
            name (str): The name of the event or collection.
            supply (int): The total number of SFTs to be created.

        Raises:
            ValueError: If a collection with the same name already exists.
        """
        if name in self._collections:
            raise ValueError(f"SFT collection '{name}' already exists.")

        self._collections[name] = {
            "name": name,
            "supply": supply,
            "minted": 0  # Tracks how many have been minted
        }

    def get_sft_collection(self, name: str):
        """
        Retrieves an SFT collection by its name.

        Args:
            name (str): The name of the collection to retrieve.

        Returns:
            dict: A dictionary containing the collection's details, or None if not found.
        """
        return self._collections.get(name)

    def get_all_collections(self):
        """
        Retrieves all created SFT collections.

        Returns:
            dict: A dictionary of all SFT collections.
        """
        return self._collections
