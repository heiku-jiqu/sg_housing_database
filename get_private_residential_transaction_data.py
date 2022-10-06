import requests
from pprint import pprint
import pandas as pd
import json
import datetime
import typing
import concurrent.futures


def read_access_key_json(path: str = "config/keys.json") -> str:
    with open(path) as f:
        access_key = json.load(f)["ura_access_key"]
    return access_key


def get_api_token(headers: dict) -> str:
    token_request = requests.get(
        "https://www.ura.gov.sg/uraDataService/insertNewToken.action", headers=headers
    )
    return token_request.json()["Result"]


def download_private_residential_data(batch: int, headers: dict):
    params = {"service": "PMI_Resi_Transaction", "batch": batch}
    print(f"fetching batch {i}")
    data_batch_i = requests.get(
        url="https://www.ura.gov.sg/uraDataService/invokeUraDS",
        params=params,
        headers=headers,
    )

    if data_batch_i.text.startswith("<!DOCTYPE html>"):
        raise Exception(
            "Fetched data not a valid JSON. Check if User-Agent is specified manually."
        )

    print(f"writing batch {batch} to file")
    folder_path = "raw_data/private_residential_transactions"
    with open(
        f"{folder_path}/batch_{batch}_{datetime.date.today()}.json",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(data_batch_i.text)


if __name__ == "__main__":
    access_key = read_access_key_json()
    headers = {
        "AccessKey": access_key,
        "User-Agent": "PostmanRuntime/7.29.0",  # IMPORTANT: explicitly set user-agent if not API wont work!
    }
    token = get_api_token(headers)
    headers.update(Token=token)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(1, 5):
            executor.submit(download_private_residential_data, i, headers)


# curl "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1" -H "AccessKey:access_key" -H "Token:token" > batch1.json
