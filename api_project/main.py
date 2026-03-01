from fastapi import FastAPI
import router

app = FastAPI(title="Blockchain API Service")

@app.get("/")
def read_root():
    return {"message": "Welcome to Blockchain API Service. See /docs for usage."}

app.include_router(router.router)

