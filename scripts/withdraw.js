const ethersMod = require('ethers');
const ethers = ethersMod.ethers ? ethersMod.ethers : ethersMod;
const fs = require('fs');

async function main() {
  const [proofsPath, contractAddress, userKey, rpcUrl] = process.argv.slice(2);
  if (!proofsPath || !contractAddress || !userKey || !rpcUrl) {
    console.log('Usage: node withdraw.js <proofs.json> <contractAddress> <userPrivateKey> <rpcUrl>');
    return;
  }

  const proofsFile = JSON.parse(fs.readFileSync(proofsPath));
  const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(userKey, provider);
  const info = proofsFile.proofs[wallet.address.toLowerCase()];
  if (!info) {
    throw new Error('No proof for this address');
  }
  const abi = ['function withdraw(uint256, bytes32[])'];
  const distributor = new ethers.Contract(contractAddress, abi, wallet);
  const tx = await distributor.withdraw(info.amount, info.proof);
  await tx.wait();
  console.log('Withdraw tx hash:', tx.hash);
}

main().catch(err => { console.error(err); process.exit(1); });
