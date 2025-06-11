import os

from rucio.client import Client
from dotenv import load_dotenv

load_dotenv()

RUCIO_HOST = os.getenv("RUCIO_HOST")
AUTH_HOST = os.getenv("AUTH_HOST")
ACCOUNT = os.getenv("ACCOUNT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

client = Client(
    rucio_host = RUCIO_HOST,
    auth_host = AUTH_HOST,
    account = ACCOUNT,
    auth_type = "userpass",
    creds = {
        "username": USERNAME,
        "password": PASSWORD,
    }
)

def get_replicas(scope, name):
    replicas = []
    
    did = [{'scope': scope, 'name': name}]
    
    for r in client.list_replicas(did):
        replicas.extend(r['rses'].keys())
        
    return replicas

print(get_replicas('user.atroja', 'test_TPC'))