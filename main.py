from fastapi import FastAPI
from api.rucio import get_rse
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI()

# Allow specific origin
origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/rse")
async def get_rse_endpoint(scope: str, name: str):
    """
    Endpoint to retrieve RSEs for a given scope and name.
    """

    rse = get_rse(scope, name)

    return rse

# print(get_rse('user.atroja', 'test_TPC'))