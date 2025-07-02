"""Rucio API connector module for interacting with Rucio client and FastAPI."""

from typing import Any

from fastapi import HTTPException, status
from rucio.client import Client

from config import get_settings

settings = get_settings()

# Create Rucio client
client = Client(
    rucio_host=settings.RUCIO_HOST,
    auth_host=settings.AUTH_HOST,
    account=settings.ACCOUNT,
    auth_type="userpass",
    creds={
        "username": settings.USERNAME,
        "password": settings.PASSWORD,
    },
)


def get_rses(did_scope: str, did_name: str) -> list[dict[str, Any]]:
    """Retrieve the list of RSEs (Rucio Storage Elements) for a given DID (Data ID).

    Args:
        did_scope (str): The scope of the DID.
        did_name (str): The name of the DID.

    Returns:
        list: A list of RSE names where the DID is replicated.

    Raises:
        HTTPException: If an error occurs while retrieving replicas.

    """
    try:
        rse = []
        did = [{"scope": did_scope, "name": did_name}]

        for r in client.list_replicas(did):
            rse.extend(r.get("rses", {}).keys())

        return rse
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
