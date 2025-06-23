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


@app.get("/rse")
async def get_rse_endpoint(did_scope: str, did_name: str):
    """
    Endpoint to retrieve RSEs for a given did scope and name.
    """

    rse = get_rse(did_scope, did_name)

    return rse


# print(get_rse('user.atroja', 'test_TPC'))
