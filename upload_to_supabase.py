import requests
import json
from io import BytesIO
import pyarrow.parquet as pq


def get_supabase_configs():
    with open("config/keys.json") as f:
        return json.load(f)["supabase"]


configs = get_supabase_configs()
filepath = "raw_data/resale_hdb/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.parquet.zstd"
filename = "resale.parquet.zstd"
url = f"{configs['endpoint']}/storage/v1/object/sg-housing-db/{filename}"
res = requests.post(
    url=url,
    headers={
        "apikey": configs["config"]["service_key"],
        "authorization": f'Bearer {configs["config"]["service_key"]}',
    },
    files={
        "resale.parquet.zstd": (
            "hello",
            open(filepath, "rb"),
            "application/octet-stream",
        )
    },
)
print(res.content)

priv_filename = (
    "raw_data/private_residential_transactions/batch_1_2023-03-23.parquet.zstd"
)
url = f"{configs['endpoint']}/storage/v1/object/sg-housing-db/batch_1_2023-03-23.parquet.zstd"

table = pq.read_table(priv_filename)

f = BytesIO()
# writer = pq.ParquetWriter(f, table.schema)
# writer.write_table(table)
# writer.close() # close writer before seeking to 0
pq.write_table(table, f)
f.seek(0)  # seek to 0 so requests can .read() from the start of buffer
res = requests.post(
    url=url,
    headers={
        "apikey": configs["config"]["service_key"],
        "authorization": f'Bearer {configs["config"]["service_key"]}',
    },
    files={
        "batch_1_2023-03-23.parquet.zstd": (
            "batch_1_2023-03-23.parquet.zstd",
            f,
            "application/octet-stream",
        )
    },
)
print(res.content)