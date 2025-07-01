// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
// import "@openzeppelin/contracts/utils/Strings.sol"; // For string conversions if needed for URI

/**
 * @title ExploreonSFT
 * @dev Basic ERC1155 Semi-Fungible Token for Exploreon experiences.
 * Each token ID can represent a unique experience or a category of experiences.
 * Metadata will point to details of the experience (event, location, timestamp).
 */
contract ExploreonSFT is ERC1155, Ownable {
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
     * @dev Constructor sets the initial base URI for token metadata.
     * The owner is set by Ownable constructor.
     */
    constructor(string memory initialBaseURI, address initialOwner) ERC1155("") Ownable(initialOwner) {
        _baseURI = initialBaseURI;
    }

    /**
     * @dev Sets the base URI for token metadata. Only callable by the owner.
     * URI should end with a trailing slash if IDs are appended directly.
     * Example: "https://api.exploreon.com/meta/sft/"
     */
    function setBaseURI(string memory newBaseURI) public onlyOwner {
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
        // string memory currentBaseURI = _baseURIextended();
        // return string(abi.encodePacked(currentBaseURI, Strings.toString(tokenId)));
        // Using Strings.toString requires importing "@openzeppelin/contracts/utils/Strings.sol".
        // For simplicity if IDs are hex or if server handles plain numbers:
        // This is a simplified placeholder. A robust solution handles hex/decimal IDs and potential URI structures.
        // OpenZeppelin's default ERC1155 URI often expects {id} to be replaced in the base URI,
        // e.g., if _baseURI is "https://myapi.com/token/{id}.json".
        // If _baseURI is just a path like "https://myapi.com/token/", then manual concatenation is needed.

        // Placeholder: assumes server handles ID, or _baseURI is structured like "https://.../{id}.json"
        // For this example, let's assume _baseURI is "https://api.exploreon.com/sfts/" and we append ID.
        // A more complex URI construction might be needed depending on metadata server requirements.
        string memory currentBaseURI = _baseURIextended();
        return string(abi.encodePacked(currentBaseURI, _uint2str(tokenId), ".json"));
    }

    /**
     * @dev Helper to convert uint to string for URI concatenation.
     * This is a basic version; for production, consider OpenZeppelin's Strings library.
     */
    function _uint2str(uint256 _i) internal pure returns (string memory str) {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 length;
        while (j != 0) {
            length++;
            j /= 10;
        }
        bytes memory bstr = new bytes(length);
        uint256 k = length;
        j = _i;
        while (j != 0) {
            bstr[--k] = bytes1(uint8(48 + j % 10));
            j /= 10;
        }
        str = string(bstr);
    }

    /**
     * @dev Mints new SFTs for a verified experience.
     * Only callable by an authorized address (e.g., system, event organizer, or owner).
     * For this basic version, only the contract owner can mint.
     * `data` can include additional verification details or user-specific info.
     *
     * @param account The address to receive the SFT.
     * @param tokenId The ID of the experience token to mint.
     * @param amount The quantity of the token to mint (typically 1 for unique experiences).
     * @param data Additional data to pass to the minting function (and hooks).
     */
    function mintExperienceToken(address account, uint256 tokenId, uint256 amount, bytes memory data) public onlyOwner {
        // Could add a check: require(experienceVerifier[tokenId] != address(0), "Experience not registered");
        // Or: require(msg.sender == experienceVerifier[tokenId], "Not authorized verifier for this experience");

        _mint(account, tokenId, amount, data);
        emit ExperienceTokenMinted(account, tokenId, amount, data);
    }

    /**
     * @dev Registers a new type of experience (a new token ID).
     * This function could be used to define what a token ID represents before minting.
     * Associates the token ID with a verifier address.
     *
     * @param tokenId The new token ID to register for an experience.
     * @param verifier The address authorized to verify/mint this specific experience token.
     * @param tokenSpecificURI Part of the URI specific to this token, if not just the ID. (optional)
     */
    function registerExperienceType(uint256 tokenId, address verifier, string memory tokenSpecificURI) public onlyOwner {
        require(experienceVerifier[tokenId] == address(0), "Experience ID already registered");
        // For this example, `tokenSpecificURI` is not directly used if `uri` function constructs from `_baseURI` and `tokenId`.
        // It's included to show how one might store more granular URI info if needed.
        experienceVerifier[tokenId] = verifier;
        // The main URI is constructed in the `uri` function.
        // If `tokenSpecificURI` was meant to be the full URI, the logic in `uri` would need to change.
        emit ExperienceRegistered(tokenId, verifier, uri(tokenId)); // Emit with the constructed URI
    }

    // The following functions are overrides required by Solidity.
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC1155, Ownable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    // Note: For actual deployment, consider security best practices:
    // - Reentrancy guards if there are complex interactions.
    // - Thorough testing and audits.
    // - Gas optimization for frequently called functions.
    // - Proper access control for sensitive functions beyond onlyOwner if needed (e.g., Role-Based Access Control).
}
