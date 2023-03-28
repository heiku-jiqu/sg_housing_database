import requests
import json
from io import BytesIO, RawIOBase
import pyarrow.parquet as pq


def get_supabase_configs():
    with open("config/keys.json") as f:
        return json.load(f)["supabase"]


def upload_file_to_supabase(
    config, bucket: str, filename: str, file: RawIOBase
) -> requests.Response:
    url = f"{config['endpoint']}/storage/v1/object/{bucket}/{filename}"
    res = requests.post(
        url=url,
        headers={
            "apikey": config["config"]["service_key"],
            "authorization": f'Bearer {config["config"]["service_key"]}',
        },
        files={
            filename: (
                filename,
                file,
                "application/octet-stream",
            )
        },
    )
    return res


configs = get_supabase_configs()
bucket = "sg-housing-db"
filepath = "raw_data/resale_hdb/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.parquet.zstd"
file = open(filepath, "rb")
filename = "resale.parquet.zstd"
res = upload_file_to_supabase(configs, bucket, filename, file)
print(res.content)

priv_filename = (
    "raw_data/private_residential_transactions/batch_1_2023-03-23.parquet.zstd"
)
table = pq.read_table(priv_filename)
f = BytesIO()
# writer = pq.ParquetWriter(f, table.schema)
# writer.write_table(table)
# writer.close() # close writer before seeking to 0
pq.write_table(table, f)
f.seek(0)  # seek to 0 so requests can .read() from the start of buffer

res = upload_file_to_supabase(configs, bucket, "batch_1_2023-03-23.parquet.zstd", f)
print(res.content)
