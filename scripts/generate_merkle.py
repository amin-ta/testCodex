import json
import sys
from typing import List, Dict
from eth_hash.auto import keccak


def keccak_hex(data: bytes) -> bytes:
    return keccak(data)


def build_tree(leaves: List[bytes]) -> List[List[bytes]]:
    """Return a list of levels, bottom (leaves) first."""
    tree = [leaves]
    level = leaves
    while len(level) > 1:
        if len(level) % 2 == 1:
            level = level + [level[-1]]
        level = [keccak_hex(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        tree.append(level)
    return tree


def get_proof(tree: List[List[bytes]], index: int) -> List[bytes]:
    proof = []
    for level in tree[:-1]:
        if len(level) % 2 == 1:
            level = level + [level[-1]]
        pair_index = index ^ 1
        proof.append(level[pair_index])
        index //= 2
    return proof


def main():
    """Generate Merkle root from a JSON mapping of address to cumulative amount."""
    if len(sys.argv) != 2:
        print("Usage: generate_merkle.py <balances.json>")
        return
    data = json.load(open(sys.argv[1]))
    addresses = list(data.keys())
    leaves = []
    for addr, amount in data.items():
        addr_bytes = bytes.fromhex(addr[2:])
        padded = b"\x00" * 12 + addr_bytes
        leaves.append(keccak_hex(padded + int(amount).to_bytes(32, "big")))
    tree = build_tree(leaves)
    root = tree[-1][0]
    proofs: Dict[str, Dict[str, object]] = {}
    for idx, addr in enumerate(addresses):
        proof = [p.hex() for p in get_proof(tree, idx)]
        proofs[addr.lower()] = {
            "amount": int(data[addr]),
            "proof": proof,
        }
    out = {"root": root.hex(), "proofs": proofs}
    json.dump(out, open("proofs.json", "w"), indent=2)
    print("Merkle root:", root.hex())
    print("Proofs written to proofs.json")


if __name__ == "__main__":
    main()
