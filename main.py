from fastapi import FastAPI
from api.rucio import get_replicas
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/replicas")
async def get_replicas_endpoint(scope: str, name: str):
    """
    Endpoint to retrieve replicas for a given scope and name.
    """
    
    replicas = get_replicas(scope, name)
    
    return replicas

# print(get_replicas('user.atroja', 'test_TPC'))