# Fast Web3 Project

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
5. **Update `.env`:** Copy the deployed contract address printed in the terminal and update the `CONTRACT_ADDRESS` variable in your root `.env` file.

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
4. **Run the API:** Start the Uvicorn server:
   ```bash
   uvicorn main:app --reload
   ```
5. **Testing the API:**
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the Swagger UI.
   - You can use the `GET /data` endpoint to read the current state of the blockchain.
   - You can use the `POST /data` endpoint with a JSON body `{"data": "Your Message"}` to write new data to the blockchain.

---

## 2. Smart Contract Logic

The smart contract (`contracts_project/contracts/DataStorage.sol`) is written in Solidity `^0.8.20`. It is a simple storage contract intended to demonstrate basic read and write operations on the blockchain.

### Core Components:
- **`string private data`**:
  A private state variable that holds a string of text. Since it is stored on the Ethereum blockchain, changing this value requires a transaction and costs gas.

- **`event DataStored(string newData)`**:
  An event that is emitted every time the `data` variable is updated. Events are crucial in DApps because they allow external consumers (like frontends or indexers) to efficiently listen for changes on the blockchain without constantly polling the contract.

- **`function setData(string memory _data) public`**:
  A function that modifies the blockchain's state. It accepts a string `_data`, updates the `data` state variable, and emits the `DataStored` event. Calling this function requires a signed transaction and consumes gas. 

- **`function getData() public view returns (string memory)`**:
  A function that reads the current value of the `data` state variable. Because it uses the `view` modifier, it promises not to modify the state of the blockchain. Therefore, calling this function does **not** cost any gas and does not require a signed transaction; it is a free read operation.
