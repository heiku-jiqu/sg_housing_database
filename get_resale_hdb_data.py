import requests
from pyarrow import Table
import pyarrow.parquet as pq
from enum import Enum


class ResourceID(Enum):
    JAN2017_ONWARDS = "f1765b54-a209-4718-8d38-a39237f502b3"
    JAN2015_TO_DEC2017 = "1b702208-44bf-4829-b620-4615ee19b57c"
    MAR2012_TO_DEC2014 = "83b2fc37-ce8c-4df4-968b-370fd818138b"
    JAN2000_TO_FEB2012 = "8c00bf08-9124-479e-aeca-7cc411d884c4"
    JAN1990_TO_JAN1999 = "adbbddd3-30e2-445f-a123-29bee150a6fe"


def request_resale_hdb_data():
    data_gov_url = "https://data.gov.sg/api/action/datastore_search"

    params = {
        "resource_id": ResourceID.JAN2017_ONWARDS.value,
        "limit": 1,
        "sort": "month",
    }
    response_current_total = requests.get(url=data_gov_url, params=params)
    current_total = response_current_total.json()["result"]["total"]
    params.update(limit=current_total)
    response = requests.get(url=data_gov_url, params=params)
    return response


if __name__ == "__main__":
    folder_path = "raw_data/resale_hdb"
    filename = "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards"

    print("fetching resale hdb data")
    response = request_resale_hdb_data()

    # write to json file
    print("writing resale hdb data to json file")
    with open(f"{folder_path}/{filename}.json", "wb") as f:
        f.write(response.content)

    # write to parquet file
    print("writing resale hdb data to parquet zstd file")
    pa_table = Table.from_pylist(response.json()["result"]["records"])
    pq.write_table(
        pa_table, f"{folder_path}/{filename}.parquet.zstd", compression="zstd"
    )
