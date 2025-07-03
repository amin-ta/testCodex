// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

/// @title RewardDistributor
/// @notice Users can withdraw rewards proved by a Merkle root of cumulative balances.
contract RewardDistributor is Ownable {
    IERC20 public immutable rewardToken;
    bytes32 public merkleRoot;
    mapping(address => uint256) public claimed;

    event RootUpdated(bytes32 root);
    event Withdraw(address indexed user, uint256 amount);

    constructor(IERC20 _token) Ownable(msg.sender) {
        rewardToken = _token;
    }

    /// @notice Owner updates the Merkle root representing cumulative user balances.
    function setMerkleRoot(bytes32 _root) external onlyOwner {
        merkleRoot = _root;
        emit RootUpdated(_root);
    }

    /// @notice Withdraw available rewards by providing a valid Merkle proof.
    /// @param cumulativeAmount Total reward earned so far for the caller.
    /// @param proof Merkle proof showing caller and amount are part of the root.
    function withdraw(uint256 cumulativeAmount, bytes32[] calldata proof) external {
        bytes32 leaf = keccak256(abi.encode(msg.sender, cumulativeAmount));
        require(MerkleProof.verify(proof, merkleRoot, leaf), "Invalid proof");
        uint256 alreadyClaimed = claimed[msg.sender];
        require(cumulativeAmount > alreadyClaimed, "Nothing to claim");
        uint256 claimable = cumulativeAmount - alreadyClaimed;
        claimed[msg.sender] = cumulativeAmount;
        require(rewardToken.transfer(msg.sender, claimable), "Transfer failed");
        emit Withdraw(msg.sender, claimable);
    }
}
