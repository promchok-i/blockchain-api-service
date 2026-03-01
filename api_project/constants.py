import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

abi_file_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
with open(abi_file_path, 'r') as f:
    CONTRACT_ABI = json.load(f)

# Initialize Web3 and Contract
w3 = None
contract = None

if ALCHEMY_URL and CONTRACT_ADDRESS:
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    if w3.is_connected():
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        print(f"Web3 connected. Contract at {CONTRACT_ADDRESS}")
    else:
        print("Warning: Failed to connect to Web3 provider.")
else:
    print("Warning: ALCHEMY_URL or CONTRACT_ADDRESS missing from .env")
