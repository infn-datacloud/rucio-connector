from fastapi import FastAPI
from api.rucio import get_replicas
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class ReplicaRequest(BaseModel):
    scope: str
    name: str

@app.post("/replicas")
async def get_replicas_endpoint(data: ReplicaRequest):
    """
    Endpoint to retrieve replicas using scope and name from the request body.
    """
    replicas = get_replicas(data.scope, data.name)
    
    return replicas