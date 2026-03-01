from fastapi import FastAPI
import router

app = FastAPI(title="Fast Web3 API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Fast Web3 API. See /docs for usage."}

app.include_router(router.router)

