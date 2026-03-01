import os
import json
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from web3 import Web3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    ALCHEMY_URL: str | None = None
    PRIVATE_KEY: str | None = None
    CONTRACT_ADDRESS: str | None = None

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

ALCHEMY_URL = settings.ALCHEMY_URL
PRIVATE_KEY = settings.PRIVATE_KEY
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS

logger.info(f"ALCHEMY_URL set: {bool(ALCHEMY_URL)}")
logger.info(f"CONTRACT_ADDRESS set: {bool(CONTRACT_ADDRESS)}")
logger.info(f"PRIVATE_KEY set: {bool(PRIVATE_KEY)}")

# Load ABI
CONTRACT_ABI = None
abi_file_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
try:
    with open(abi_file_path, 'r') as f:
        CONTRACT_ABI = json.load(f)
    logger.info(f"ABI loaded from {abi_file_path}")
except Exception as e:
    logger.error(f"Failed to load ABI from {abi_file_path}: {e}")

# Initialize Web3 and Contract
w3 = None
contract = None

if ALCHEMY_URL and CONTRACT_ADDRESS and CONTRACT_ABI:
    try:
        w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
        if w3.is_connected():
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            logger.info(f"Web3 connected. Contract at {CONTRACT_ADDRESS}")
        else:
            logger.warning("Web3 provider not connected. Initializing contract anyway.")
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    except Exception as e:
        logger.error(f"Failed to initialize Web3/Contract: {e}")
else:
    logger.warning(f"Missing config - ALCHEMY_URL: {bool(ALCHEMY_URL)}, CONTRACT_ADDRESS: {bool(CONTRACT_ADDRESS)}, ABI: {bool(CONTRACT_ABI)}")
