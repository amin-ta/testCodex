# MLOps System Example

This repository provides a small demonstration of how an MLOps service might
handle image datasets and training jobs. It uses **Flask** for the API layer and
**ultralytics** for YOLO model training.

## Structure

- `mlops_system/` contains the application modules:
 - `app.py` – Flask server exposing dataset and training endpoints and serving a small web UI.
  - `dataset.py` – utilities for uploading, listing and merging datasets.
  - `training.py` – wrapper that launches YOLO training.
  - `auth.py` – very simple token based authentication helper.

Datasets are stored under the `datasets/` directory created at runtime.

## Usage

Install the required packages and run the server. The root page `/` provides a simple browser UI for uploading datasets and starting training jobs:


```bash
pip install flask ultralytics
python -m mlops_system.app
```

The API accepts an `Authorization` header matching a token from `mlops_system.auth.USERS`.

Example endpoints:

- `POST /upload` – form-data with `file` (zip) and `name` parameters.
- `GET /datasets` – list available datasets.
- `POST /datasets/merge` – JSON body `{ "names": [..], "format": "zip" }`.
- `POST /datasets/<name>/train` – JSON body `{ "val_split": 0.2 }` to start YOLO training.

You can also use the web interface at `/` instead of calling the endpoints manually.

This project is a minimal skeleton and does not implement advanced features such
as user permissions, searching by object labels or a production-ready auth
system. It can be extended to meet specific company requirements.

## Reward Distribution Contract

The `contracts/RewardDistributor.sol` smart contract allows users to
withdraw rewards that are published off-chain via a Merkle root. Each
day you recompute cumulative balances for all users, generate a new
root and call `setMerkleRoot` with it. Users prove their balance using a
Merkle proof when calling `withdraw`.

Helper scripts are provided to publish a new Merkle root. You can use the
Python script `scripts/generate_merkle.py` or the Node version
`scripts/generateMerkle.js`. Both read a JSON mapping of addresses to
cumulative amounts and produce `proofs.json`.

Python usage:

```bash
pip install eth-hash
python scripts/generate_merkle.py balances.json
```

Node usage (also pushes the root on-chain if parameters are given):

```bash
npm install
node scripts/generateMerkle.js balances.json <contract> <ownerKey> <rpcUrl>
```

Deploy `RewardDistributor.sol` passing the ERC20 token used for rewards
(for example the USDC token address on Polygon).
Only the owner can update the root. Users can withdraw at any time with
proofs corresponding to the latest root.

### Generating a proof

`generate_merkle.py` now also creates a `proofs.json` file that stores the
Merkle proof for each address alongside the cumulative amount. Run the script
with your balances file:

```bash
python scripts/generate_merkle.py balances.json
```

The command prints the Merkle root and writes `proofs.json` in the same
directory.

### Sending a withdraw transaction

Load the user's proof from `proofs.json` and call `withdraw` using the helper
script:

```bash
node scripts/withdraw.js proofs.json <contract> <userKey> <rpcUrl>
```

Internally it performs the equivalent of:

```javascript
const proofs = require('./proofs.json');
const distributor = new ethers.Contract(address, RewardDistributorAbi, signer);
const { amount, proof } = proofs[signer.address.toLowerCase()];
await distributor.withdraw(amount, proof);
```

`signer` is the connected wallet (for example MetaMask). The contract verifies
the proof and transfers the pending rewards.
