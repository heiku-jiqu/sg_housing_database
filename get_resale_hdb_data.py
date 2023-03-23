import requests
from pyarrow import Table
import pyarrow.parquet as pq


def request_resale_hdb_data():
    resource_id = {
        "2017 onwards": "f1765b54-a209-4718-8d38-a39237f502b3",
        "Jan 2015 - Dec 2016": "1b702208-44bf-4829-b620-4615ee19b57c",
        "Mar 2012 - Dec 2014": "83b2fc37-ce8c-4df4-968b-370fd818138b",
        "2000 - Feb 2012": "8c00bf08-9124-479e-aeca-7cc411d884c4",
        "1990 - 1999": "adbbddd3-30e2-445f-a123-29bee150a6fe",
    }
    data_gov_url = "https://data.gov.sg/api/action/datastore_search"

    params = {
        "resource_id": resource_id["2017 onwards"],
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
