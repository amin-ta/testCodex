const ethersMod = require('ethers');
const ethers = ethersMod.ethers ? ethersMod.ethers : ethersMod;
const { MerkleTree } = require('merkletreejs');
const keccak256 = require('keccak256');
const fs = require('fs');

function abiEncode(types, values) {
  if (ethers.utils && ethers.utils.defaultAbiCoder) {
    return ethers.utils.defaultAbiCoder.encode(types, values);
  }
  const coder = ethers.AbiCoder && ethers.AbiCoder.defaultAbiCoder
    ? ethers.AbiCoder.defaultAbiCoder()
    : new ethers.AbiCoder();
  return coder.encode(types, values);
}

function leafHash(addr, amount) {
  const encoded = abiEncode(['address', 'uint256'], [addr, amount]);
  if (ethers.utils && ethers.utils.keccak256) {
    return ethers.utils.keccak256(encoded);
  }
  return ethers.keccak256(encoded);
}

async function main() {
  const [balancesPath, contractAddress, ownerKey, rpcUrl] = process.argv.slice(2);
  if (!balancesPath) {
    console.log('Usage: node generateMerkle.js <balances.json> [contractAddress ownerKey rpcUrl]');
    return;
  }

  const data = JSON.parse(fs.readFileSync(balancesPath));
  const addresses = Object.keys(data);
  const leaves = addresses.map(addr => leafHash(addr, data[addr]));
  const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });
  const root = tree.getHexRoot();

  const proofs = {};
  addresses.forEach((addr, i) => {
    proofs[addr.toLowerCase()] = {
      amount: parseInt(data[addr]),
      proof: tree.getHexProof(leaves[i])
    };
  });

  fs.writeFileSync('proofs.json', JSON.stringify({ root, proofs }, null, 2));
  console.log('Merkle root:', root);
  console.log('Proofs written to proofs.json');

  if (contractAddress && ownerKey && rpcUrl) {
    const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
    const wallet = new ethers.Wallet(ownerKey, provider);
    const abi = ['function setMerkleRoot(bytes32)'];
    const distributor = new ethers.Contract(contractAddress, abi, wallet);
    const tx = await distributor.setMerkleRoot(root);
    await tx.wait();
    console.log('Root updated on-chain:', tx.hash);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
