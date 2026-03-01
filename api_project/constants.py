import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

ALCHEMY_URL = os.getenv("ALCHEMY_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

abi_file_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
with open(abi_file_path, 'r') as f:
    CONTRACT_ABI = json.load(f)
