from rucio.client import Client

client = Client(
    rucio_host = "https://rucio.192.135.24.152.myip.cloud.infn.it",
    auth_host = "https://rucio-auth.192.135.24.152.myip.cloud.infn.it",
    account = "etserra",
    auth_type = "userpass",
    creds = {
        "username": "etserra",
        "password": "etserrapwd",
    }
)

def get_replicas(scope, name):
    replicas = []
    
    did = [{'scope': scope, 'name': name}]
    
    for r in client.list_replicas(did):
        replicas.extend(r['rses'].keys())
        
    return replicas

print(get_replicas('user.atroja', 'test_TPC'))