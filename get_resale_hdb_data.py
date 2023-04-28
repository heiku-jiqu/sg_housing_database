import requests
import pyarrow as pa
from pyarrow import Table
import pyarrow.parquet as pq
from enum import Enum
from typing import List


class ResourceID(Enum):
    JAN2017_ONWARDS = "f1765b54-a209-4718-8d38-a39237f502b3"
    JAN2015_TO_DEC2017 = "1b702208-44bf-4829-b620-4615ee19b57c"
    MAR2012_TO_DEC2014 = "83b2fc37-ce8c-4df4-968b-370fd818138b"
    JAN2000_TO_FEB2012 = "8c00bf08-9124-479e-aeca-7cc411d884c4"
    JAN1990_TO_JAN1999 = "adbbddd3-30e2-445f-a123-29bee150a6fe"


def request_resale_hdb_data(resource_id: ResourceID = ResourceID.JAN2017_ONWARDS):
    print(f"fetching {resource_id}")
    data_gov_url = "https://data.gov.sg/api/action/datastore_search"

    params = {
        "resource_id": resource_id.value,
        "limit": 1,
        "sort": "month",
    }
    response_current_total = requests.get(url=data_gov_url, params=params)
    current_total = response_current_total.json()["result"]["total"]
    params.update(limit=current_total)
    response = requests.get(url=data_gov_url, params=params)
    return response


JAN2017_ONWARDS_PA_SCHEMA = pa.schema(
    [
        ("town", pa.string()),
        ("flat_type", pa.string()),
        ("flat_model", pa.string()),
        ("floor_area_sqm", pa.float32()),
        ("street_name", pa.string()),
        ("resale_price", pa.float32()),
        ("month", pa.string()),
        ("remaining_lease", pa.string()),
        ("lease_commence_date", pa.string()),
        ("storey_range", pa.string()),
        ("_id", pa.int32()),
        ("block", pa.string()),
    ]
)

JAN1990_TO_DEC2014_PA_SCHEMA = pa.schema(
    [
        ("town", pa.string()),
        ("flat_type", pa.string()),
        ("flat_model", pa.string()),
        ("floor_area_sqm", pa.float32()),
        ("street_name", pa.string()),
        ("resale_price", pa.float32()),
        ("month", pa.string()),
        ("lease_commence_date", pa.string()),
        ("storey_range", pa.string()),
        ("_id", pa.int32()),
        ("block", pa.string()),
    ]
)


def dict_encode_cols(
    table: pa.Table, columns: List[str] = ["town", "flat_type", "flat_model"]
) -> pa.Table:
    res = table
    for col in columns:
        res = dict_encode_col(res, col)
    return res


def dict_encode_col(table: pa.Table, col: str) -> pa.Table:
    table.set_column(
        table.column_names.index(col),
        col,
        table.column(col).dictionary_encode(),
    )
    return table


if __name__ == "__main__":
    folder_path = "raw_data/resale_hdb"
    filename = "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards"

    print("fetching JAN2017_ONWARDS resale hdb data")
    response = request_resale_hdb_data()

    # write to json file
    print("writing JAN2017_ONWARDS resale hdb data to json file")
    with open(f"{folder_path}/{filename}.json", "wb") as f:
        f.write(response.content)

    # write to parquet file
    print("writing JAN2017_ONWARDS resale hdb data to parquet zstd file")
    pa_table = Table.from_pylist(response.json()["result"]["records"])
    pq.write_table(
        pa_table, f"{folder_path}/{filename}.parquet.zstd", compression="zstd"
    )

    pa_table_dict_encoded = dict_encode_cols(pa_table.cast(JAN2017_ONWARDS_PA_SCHEMA))

    pq.write_table(
        pa_table_dict_encoded,
        f"{folder_path}/{filename}_dict_enc.parquet.zstd",
        compression="zstd",
    )

    print("fetching JAN2015 TO DEC2017 Data")
    res2 = request_resale_hdb_data(ResourceID.JAN2015_TO_DEC2017)
    pa_table2 = Table.from_pylist(res2.json()["result"]["records"])
    pa_table2_dict_encoded = dict_encode_cols(pa_table2.cast(JAN2017_ONWARDS_PA_SCHEMA))

    print("fetching MAR2012 TO DEC2014 Data")
    res3 = request_resale_hdb_data(ResourceID.MAR2012_TO_DEC2014)
    pa_table3 = Table.from_pylist(res3.json()["result"]["records"])
    pa_table3_dict_encoded = dict_encode_cols(
        pa_table3.cast(JAN1990_TO_DEC2014_PA_SCHEMA)
    )
    print("fetching JAN2000 TO FEB2012 Data")
    res4 = request_resale_hdb_data(ResourceID.JAN2000_TO_FEB2012)
    pa_table4 = Table.from_pylist(res4.json()["result"]["records"])
    pa_table4_dict_encoded = dict_encode_cols(
        pa_table4.cast(JAN1990_TO_DEC2014_PA_SCHEMA)
    )
    print("fetching JAN1990 TO DEC1999 Data")
    res5 = request_resale_hdb_data(ResourceID.JAN1990_TO_JAN1999)
    pa_table5 = Table.from_pylist(res5.json()["result"]["records"])
    pa_table5_dict_encoded = dict_encode_cols(
        pa_table5.cast(JAN1990_TO_DEC2014_PA_SCHEMA)
    )
