import requests
import urllib.request
from pprint import pprint
import pandas as pd
import json

folder_path = 'raw_data/private_residential_transactions'

with open('config/keys.json') as f:
    access_key = json.load(f)['ura_access_key']

headers = {
    'AccessKey': access_key,
    'User-Agent': '' # IMPORTANT: explicitly set user-agent if not API wont work!
}
token_request = requests.get(
    "https://www.ura.gov.sg/uraDataService/insertNewToken.action",
    headers = headers
)
token = token_request.json()["Result"]

headers.update(Token=token)
service = 'PMI_Resi_Transaction'
params = {
    'service': service,
    'batch': 1
}
for i in range(1,5):
    params.update(batch=i)
    data_batch_i = requests.get(
        url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS',
        params = params,
        headers = headers
    )
    with open(f'{folder_path}/batch_{i}.json', "w") as f:
        f.write(data_batch_i.text)

# curl "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1" -H "AccessKey:access_key" -H "Token:token" > batch1.json