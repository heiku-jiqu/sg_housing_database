import requests
from pprint import pprint
import pandas as pd
import json
import datetime

folder_path = "raw_data/private_residential_transactions"

with open("config/keys.json") as f:
    access_key = json.load(f)["ura_access_key"]

headers = {
    "AccessKey": access_key,
    "User-Agent": "PostmanRuntime/7.29.0",  # IMPORTANT: explicitly set user-agent if not API wont work!
}
token_request = requests.get(
    "https://www.ura.gov.sg/uraDataService/insertNewToken.action", headers=headers
)
token = token_request.json()["Result"]

headers.update(Token=token)
service = "PMI_Resi_Transaction"
params = {"service": service, "batch": 1}
for i in range(1, 5):
    print(f"fetching batch {i}")
    params.update(batch=i)
    data_batch_i = requests.get(
        url="https://www.ura.gov.sg/uraDataService/invokeUraDS",
        params=params,
        headers=headers,
    )

    if data_batch_i.text.startswith("<!DOCTYPE html>"):
        raise Exception(
            "Fetched data not a valid JSON. Check if User-Agent is specified manually."
        )

    print(f"writing batch {i} to file")
    with open(
        f"{folder_path}/batch_{i}_{datetime.date.today()}.json", "w", encoding="utf-8"
    ) as f:
        f.write(data_batch_i.text)

# curl "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1" -H "AccessKey:access_key" -H "Token:token" > batch1.json
