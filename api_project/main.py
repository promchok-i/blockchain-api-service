import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3
from dotenv import load_dotenv

# Load from the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Fast Web3 API")

ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# In production, securely load the ABI. Here we hardcode for simplicity of the tutorial.
CONTRACT_ABI = json.loads('''[
    {"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"newData","type":"string"}],"name":"DataStored","type":"event"},
    {"inputs":[],"name":"getData","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"string","name":"_data","type":"string"}],"name":"setData","outputs":[],"stateMutability":"nonpayable","type":"function"}
]''')

w3 = None
contract = None

@app.on_event("startup")
async def startup_event():
    global w3, contract
    if not ALCHEMY_URL or not CONTRACT_ADDRESS:
        print("Warning: Web3 credentials/contract address missing.")
        return
        
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    if not w3.is_connected():
        print("Warning: Failed to connect to Web3 provider.")
        return
        
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

class DataInput(BaseModel):
    data: str

@app.get("/data")
async def get_data():
    if not contract:
        raise HTTPException(status_code=500, detail="Web3/Contract not initialized")

    try:
        # Call the view function
        result = contract.functions.getData().call()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/data")
async def set_data(input_data: DataInput):
    if not contract or not w3:
        raise HTTPException(status_code=500, detail="Web3/Contract not initialized")
    if not PRIVATE_KEY:
        raise HTTPException(status_code=500, detail="Private key missing")

    try:
        # Get the account from private key
        account = w3.eth.account.from_key(PRIVATE_KEY)

        # Build transaction
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Estimate gas for the specific contract execution
        gas_estimate = contract.functions.setData(input_data.data).estimate_gas({'from': account.address})
        gas_price = w3.eth.gas_price

        tx = contract.functions.setData(input_data.data).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction) # Actually sends it

        # Wait for receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        return {
            "message": "Data stored successfully",
            "transaction_hash": tx_hash.hex(),
            "status": tx_receipt.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Fast Web3 API. See /docs for usage."}
