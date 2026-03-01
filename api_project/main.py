from fastapi import FastAPI
from web3 import Web3
import router
from constants import ALCHEMY_URL, CONTRACT_ADDRESS, CONTRACT_ABI

app = FastAPI(title="Fast Web3 API")

@app.on_event("startup")
async def startup_event():
    if not ALCHEMY_URL or not CONTRACT_ADDRESS:
        print("Warning: Web3 credentials/contract address missing.")
        return
        
    router.w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    if not router.w3.is_connected():
        print("Warning: Failed to connect to Web3 provider.")
        return
        
    router.contract = router.w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

@app.get("/")
def read_root():
    return {"message": "Welcome to Fast Web3 API. See /docs for usage."}

app.include_router(router.router)
