from typing import Optional
import requests
import json
from io import BytesIO, RawIOBase
import pyarrow.parquet as pq
import os


def get_supabase_configs():
    endpoint = os.environ.get("SUPABASE_ENDPOINT")
    service_key = os.environ.get("SUPABASE_SERVICE_KEY")
    if endpoint and service_key:
        return {"config": {"service_key": service_key}, "endpoint": endpoint}
    else:
        with open("config/keys.json") as f:
            return json.load(f)["supabase"]


def download_file_from_supabase(
    config, bucket: str, filename: str
) -> requests.Response:
    url = f"{config['endpoint']}/storage/v1/object/authenticated/{bucket}/{filename}"
    res = requests.get(
        url,
        headers={
            "apikey": config["config"]["service_key"],
            "authorization": f'Bearer {config["config"]["service_key"]}',
        },
    )
    return res


def upload_file_to_supabase(
    config, bucket: str, filename: str, file: RawIOBase, upsert: bool = False
) -> requests.Response:
    url = f"{config['endpoint']}/storage/v1/object/{bucket}/{filename}"
    res = requests.post(
        url=url,
        headers={
            "apikey": config["config"]["service_key"],
            "authorization": f'Bearer {config["config"]["service_key"]}',
            "x-upsert": str(upsert).lower(),
            "cache-control": "max-age=604800",
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


def list_files_from_supabase_bucket(
    config, bucket: str, prefix: str = "", filename: Optional[str] = None
) -> requests.Response:
    url = f"{config['endpoint']}/storage/v1/object/list/{bucket}"
    res = requests.post(
        url=url,
        headers={
            "apikey": config["config"]["service_key"],
            "authorization": f'Bearer {config["config"]["service_key"]}',
        },
        json={"prefix": prefix, "search": filename},
    )
    return res


if __name__ == "__main__":
    configs = get_supabase_configs()
    bucket = "sg-housing-db"

    file_info_response = list_files_from_supabase_bucket(
        configs, bucket, prefix="", filename="resale.parquet.zstd"
    )
    print(len(file_info_response.json()))

    file_info_non_response = list_files_from_supabase_bucket(
        configs, bucket, prefix="", filename="non-existent-file"
    )
    print(len(file_info_non_response.json()))

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

    res = download_file_from_supabase(configs, bucket, "resale.parquet.zstd")
    table = pq.read_table(BytesIO(res.content))
    print(table)
