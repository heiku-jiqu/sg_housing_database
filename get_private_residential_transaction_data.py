import requests
from requests import Response
import json
import datetime
import concurrent.futures
from pyarrow import Table
import pyarrow as pa
import pyarrow.parquet as pq
from typing import List


def read_access_key_json(path: str = "config/keys.json") -> str:
    with open(path) as f:
        access_key = json.load(f)["ura_access_key"]
    return access_key


def get_api_token(headers: dict) -> str:
    token_request = requests.get(
        "https://www.ura.gov.sg/uraDataService/insertNewToken.action", headers=headers
    )
    return token_request.json()["Result"]


def request_private_residential_data(batch: int, headers: dict):
    params = {"service": "PMI_Resi_Transaction", "batch": batch}
    print(f"fetching private residential data (batch {batch})")
    response = requests.get(
        url="https://www.ura.gov.sg/uraDataService/invokeUraDS",
        params=params,
        headers=headers,
    )

    if response.text.startswith("<!DOCTYPE html>"):
        raise Exception(
            "Fetched data not a valid JSON. Check if User-Agent is specified manually."
        )
    return response


def write_to_json(
    response: Response,
    batch: int,
    folder_path: str = "raw_data/private_residential_transactions",
):
    print(f"writing batch {batch} to json file")
    with open(
        f"{folder_path}/batch_{batch}_{datetime.date.today()}.json",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(response.text)


def write_to_parquet(
    response: Response,
    batch: int,
    folder_path: str = "raw_data/private_residential_transactions",
):
    print(f"writing batch {batch} to parquet zstd file")
    pa_table: Table = Table.from_pylist(response.json()["Result"])
    pq.write_table(
        pa_table,
        f"{folder_path}/batch_{batch}_{datetime.date.today()}.parquet.zstd",
        compression="zstd",
    )


def request_and_save_locally(batch, headers):
    res = request_private_residential_data(batch, headers)
    write_to_json(res, batch)
    write_to_parquet(res, batch)


def request_private_residential_data_batches_concurrent(headers) -> List[Response]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for i in range(1, 5):
            futures.update(
                {executor.submit(request_private_residential_data, i, headers): i}
            )
        results = []
        for future in futures.keys():
            batch = futures[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print(f"batch {batch} generated an exception: {exc}")
        return results


def priv_residential_data_response_to_pyarrow(res: Response) -> Table:
    return Table.from_pylist(res.json()["Result"])


if __name__ == "__main__":
    access_key = read_access_key_json()
    headers = {
        "AccessKey": access_key,
        "User-Agent": "PostmanRuntime/7.29.0",  # IMPORTANT: explicitly set user-agent if not API wont work!
    }
    token = get_api_token(headers)
    headers.update(Token=token)
    results = request_private_residential_data_batches_concurrent(headers)
    pa_tables = [
        priv_residential_data_response_to_pyarrow(response) for response in results
    ]
    joined_table = pa.concat_tables(pa_tables)
    pq.write_table(
        joined_table,
        "raw_data/private_residential_transactions/all_batches_joined.parquet.zstd",
        compression="zstd",
    )


# curl "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1" -H "AccessKey:access_key" -H "Token:token" > batch1.json
