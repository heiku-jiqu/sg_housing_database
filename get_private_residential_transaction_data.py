import requests
from pprint import pprint
import pandas as pd
import json

folder_path = 'raw_data/private_residential_transactions'

with open('config/keys.json') as f:
    access_key = json.load(f)['ura_access_key']

headers = {
    'Content-Type': 'application/json',
    'AccessKey': access_key
}

token_request = requests.get(
    url = "https://www.ura.gov.sg/uraDataService/insertNewToken.action",
    headers = headers
)
token = token_request.json()["Result"]
headers.update(Token=token)

service = 'PMI_Resi_Transaction'
params = {
    'Service': service,
    'Batch': 1
}

data_batch_1 = requests.get(
    url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS',
    params = params,
    headers=headers
)

