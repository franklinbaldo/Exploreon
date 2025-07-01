// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title ExploreonSFT
 * @dev ERC1155 Semi-Fungible Token for Exploreon experiences with AccessControl, Pausable, and ReentrancyGuard.
 * Each token ID can represent a unique experience or a category of experiences.
 * Metadata will point to details of the experience (event, location, timestamp).
 */
contract ExploreonSFT is ERC1155, AccessControl, Pausable, ReentrancyGuard {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE"); // Role for registering experiences

    // Base URI for all token types. Specific token URIs will be {baseURI}{id}.json
    string private _baseURI;

    // Mapping from token ID to the creator/verifier of the experience
    // This could be an event organizer's address or a system address
    mapping(uint256 => address) public experienceVerifier;

    // Event to log when a new experience type (token ID) is registered
    event ExperienceRegistered(uint256 indexed tokenId, address indexed verifier, string uri);

    // Event to log when an SFT is minted as proof of experience
    event ExperienceTokenMinted(address indexed account, uint256 indexed tokenId, uint256 amount, bytes data);

    /**
     * @dev Constructor sets the initial base URI for token metadata and grants roles.
     * The deployer gets admin, minter, and verifier roles.
     */
    constructor(string memory initialBaseURI, address initialAdmin) ERC1155("") {
        _baseURI = initialBaseURI;
        _grantRole(DEFAULT_ADMIN_ROLE, initialAdmin);
        _grantRole(MINTER_ROLE, initialAdmin);
        _grantRole(VERIFIER_ROLE, initialAdmin);
    }

    /**
     * @dev Sets the base URI for token metadata. Only callable by an address with DEFAULT_ADMIN_ROLE.
     * URI should end with a trailing slash if IDs are appended directly.
     * Example: "https://api.exploreon.com/meta/sft/"
     */
    function setBaseURI(string memory newBaseURI) public onlyRole(DEFAULT_ADMIN_ROLE) {
        _baseURI = newBaseURI;
    }

    /**
     * @dev Returns the base URI for token metadata.
     */
    function _baseURIextended() internal view returns (string memory) {
        return _baseURI;
    }

    /**
     * @dev Overrides ERC1155's uri function to construct the metadata URI.
     * Appends the token ID to the base URI.
     * Assumes metadata for token ID 123 is at {baseURI}123.json (if baseURI includes .json part or similar)
     * Or typically: {baseURI}{id} (e.g. OpenSea format for ERC1155)
     */
    function uri(uint256 tokenId) public view override returns (string memory) {
        string memory currentBaseURI = _baseURIextended();
        // Using OpenZeppelin's Strings.toString library
        return string(abi.encodePacked(currentBaseURI, Strings.toString(tokenId), ".json"));
    }

    /**
     * @dev Mints new SFTs for a verified experience.
     * Callable by an address with MINTER_ROLE.
     * Pauses when `whenNotPaused` is active. Non-reentrant.
     * `data` can include additional verification details or user-specific info.
     *
     * @param account The address to receive the SFT.
     * @param tokenId The ID of the experience token to mint.
     * @param amount The quantity of the token to mint (typically 1 for unique experiences).
     * @param data Additional data to pass to the minting function (and hooks).
     */
    function mintExperienceToken(address account, uint256 tokenId, uint256 amount, bytes memory data)
        public
        onlyRole(MINTER_ROLE) // General role check for calling the function
        whenNotPaused
        nonReentrant
    {
        require(experienceVerifier[tokenId] != address(0), "Experience not registered for this tokenId");
        // Specific check: The caller (who has MINTER_ROLE) must also be the registered verifier for this specific token.
        require(experienceVerifier[tokenId] == msg.sender, "Caller is not the registered verifier for this specific tokenId");

        _mint(account, tokenId, amount, data);
        emit ExperienceTokenMinted(account, tokenId, amount, data);
    }

    /**
     * @dev Registers a new type of experience (a new token ID).
     * Associates the token ID with a verifier address.
     * Only callable by an address with VERIFIER_ROLE.
     *
     * @param tokenId The new token ID to register for an experience.
     * @param verifier The address authorized to verify/mint this specific experience token.
     * @param tokenSpecificURI Part of the URI specific to this token, if not just the ID. (optional)
     */
    function registerExperienceType(uint256 tokenId, address verifier, string memory tokenSpecificURI)
        public
        onlyRole(VERIFIER_ROLE)
    {
        require(experienceVerifier[tokenId] == address(0), "Experience ID already registered");
        // For this example, `tokenSpecificURI` is not directly used if `uri` function constructs from `_baseURI` and `tokenId`.
        // It's included to show how one might store more granular URI info if needed.
        experienceVerifier[tokenId] = verifier;
        // The main URI is constructed in the `uri` function.
        // If `tokenSpecificURI` was meant to be the full URI, the logic in `uri` would need to change.
        emit ExperienceRegistered(tokenId, verifier, uri(tokenId)); // Emit with the constructed URI
    }

    /**
     * @dev Pauses all token transfers and minting. Only callable by an address with DEFAULT_ADMIN_ROLE.
     */
    function pause() public virtual onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    /**
     * @dev Unpauses all token transfers and minting. Only callable by an address with DEFAULT_ADMIN_ROLE.
     */
    function unpause() public virtual onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    // The following functions are overrides required by Solidity.
    // ERC1155's _beforeTokenTransfer and _afterTokenTransfer hooks are overridden by Pausable
    // to prevent transfers while paused. We also need to ensure minting/burning considers Pausable.

    function _update(address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        override(ERC1155, Pausable) // Pausable's _beforeTokenTransfer will be called
    {
        super._update(from, to, ids, amounts, data);
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC1155, AccessControl) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    // Note: For actual deployment, consider security best practices:
    // - Thorough testing and audits (this version includes some improvements).
    // - Gas optimization for frequently called functions.
}
