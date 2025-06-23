from fastapi import HTTPException
from rucio.client import Client
from config import get_settings

settings = get_settings()

# Create Rucio client
client = Client(
    rucio_host=bytes(settings.RUCIO_HOST, "utf-8").decode("unicode_escape"),
    auth_host=bytes(settings.AUTH_HOST, "utf-8").decode("unicode_escape"),
    account=settings.ACCOUNT,
    auth_type="userpass",
    creds={
        "username": settings.USERNAME,
        "password": settings.PASSWORD,
    }
)

def get_rse(scope, name):
    try:
        rse = []
        did = [{"scope": scope, "name": name}]

        for r in client.list_replicas(did):
            rse.extend(r.get("rses", {}).keys())

        return rse
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))