# Blockchain API Service

This project demonstrates a simple integration between a **Hardhat** smart contract environment and a **FastAPI** web service. It allows you to read from and write data to the Ethereum Sepolia Testnet using Python!

## Project Structure

The project is split into two main functional areas, but they share a single root configuration (`.env`):
- `contracts_project/`: A Hardhat project containing the Solidity smart contracts and deployment scripts.
- `api_project/`: A FastAPI Python service that connects to the deployed contract via Web3.py.
- `.env`: The root configuration file containing your Alchemy RPC URL and wallet private key.

## 1. Setup, Testing, and Deployment

### Prerequisites
- Node.js & NPM
- Python 3.8+
- An Alchemy account (for Sepolia Testnet RPC URL)
- A MetaMask wallet with some Sepolia ETH 

### Environment Configuration
1. At the root of the project, create a `.env` file (if it doesn't exist) by copying the format below:
   ```env
   # Shared credentials
   ALCHEMY_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY
   PRIVATE_KEY=your_private_key_here
   CONTRACT_ADDRESS=your_deployed_contract_address_here
   ```
2. Replace `ALCHEMY_URL` and `PRIVATE_KEY` with your actual credentials.

### Smart Contract Setup & Deployment (`contracts_project`)
1. Open a terminal and navigate to the contracts directory:
   ```bash
   cd contracts_project
   ```
2. Install the necessary Node.js dependencies:
   ```bash
   npm install
   ```
3. **Run Tests:** To verify the contract logic runs correctly locally, run the Hardhat tests:
   ```bash
   npx hardhat test
   ```
4. **Deploy to Sepolia:** Run the deployment script to push the contract to the testnet:
   ```bash
   npx hardhat run scripts/deploy.js --network sepolia
   ```
5. **Verify the Contract:** Verify the deployed smart contract on Etherscan:
   ```bash
   npx hardhat verify --network sepolia <your_deployed_contract_address_here>
   ```
6. **Update `.env`:** Copy the deployed contract address printed in the terminal and update the `CONTRACT_ADDRESS` variable in your root `.env` file.

### FastAPI Setup & Running (`api_project`)
1. Open a terminal and navigate to the API directory:
   ```bash
   cd api_project
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. **Update ABI:** Run the `update_abi.py` script to copy the updated compiled artifacts into the API:
   ```bash
   python3 update_abi.py
   ```
5. **Run the API:** Start the FastAPI dev server:
   ```bash
   fastapi dev main.py
   ```
6. **Testing the API:**
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the Swagger UI.
   - You can use the `POST /document` endpoint to store a new document with fields like `document_id`, `issuer_id`, `holder_id`, `hashed_content`, and `is_active`.
   - You can use the `GET /document/{document_id}` endpoint to retrieve a stored document.
   - You can use the `POST /documents/query` endpoint for bulk retrieval of documents.

---

## 2. Smart Contract Logic

The smart contract (`contracts_project/contracts/DocumentStorage.sol`) is written in Solidity `^0.8.20`. It enables robust, scalable on-chain document proof verification.

### Core Components:

- **`struct Document` & Storage Maps**:
  Documents are modeled using a struct containing `documentId`, `issuerId`, `holderId`, `hashedContent`, and `isActive`. These are stored in a mapping for optimized retrieval.

- **`event DocumentStored(...)`**:
  An event emitted whenever a new document is stored. Events allow external consumers (like indexers or frontends) to query and track historical data without constantly accessing contract state.

- **`function storeDocument(...) public`**:
  Modifies the blockchain's state by adding a new document into storage. It requires a signed transaction and consumes gas.

- **`function getDocument(string memory _documentId) public view returns (...)`**:
  Retrieves a specific document. Since it is a `view` function, it does not cost gas and does not require a transaction signature; it operates as a free read operation.

- **`function getDocuments(string[] memory _documentIds) public view returns (...)`**:
  Allows batch retrieval of multiple documents at once, reducing the overhead of repeated API calls.
