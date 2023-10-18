from get_private_residential_transaction_data import *
from get_resale_hdb_data import *
from supabase import *
import pyarrow as pa
from pyarrow import Table
import pyarrow.parquet as pq
from io import BytesIO
import os


if __name__ == "__main__":
    print("Processing Private Residential Data")
    access_key = os.environ.get("URA_ACCESS_KEY")
    if access_key is None:
        access_key = read_access_key_json()
    headers = {
        "AccessKey": access_key,
        "User-Agent": "PostmanRuntime/7.29.0",  # IMPORTANT: explicitly set user-agent if not API wont work!
    }
    token = get_api_token(headers)
    headers.update(Token=token)

    priv_data = request_private_residential_data_batches_concurrent(headers)

    pa_tables = [Table.from_pylist(d.json()["Result"]) for d in priv_data]
    # downloading of JAN2015-DEC2016 data failing due to datagov API bug, can only fetch up to 15706 rows even though max rows is 37153

    merged_table = pa.concat_tables(pa_tables)

    f = BytesIO()
    pq.write_table(merged_table, f, compression="zstd", compression_level=22)
    f.seek(0)

    res = upload_file_to_supabase(
        get_supabase_configs(),
        "sg-housing-db",
        "priv_residential.parquet.zstd",
        f,
        upsert=True,
    )
    print(res.content)

    print("Processing HDB Resale Data")
    hdb_req = [request_resale_hdb_data(e) for e in ResourceID]
    pa_tables = [Table.from_pylist(r.json()["result"]["records"]) for r in hdb_req]
    encoded_hdb_tables = []
    for t in pa_tables:
        if t.num_columns == 12:
            encoded_hdb_tables.append(
                dict_encode_cols(t.cast(JAN2017_ONWARDS_PA_SCHEMA))
            )
        elif t.num_columns == 11:
            encoded_hdb_tables.append(
                dict_encode_cols(t.cast(JAN1990_TO_DEC2014_PA_SCHEMA))
            )
        else:
            raise Exception("unknown schema to cast")
    merged_hdb_table = (
        pa.concat_tables(encoded_hdb_tables, promote=True)
        .drop(["_id"])
        .sort_by(
            [
                ("flat_type", "ascending"),
                ("storey_range", "ascending"),
                ("town", "ascending"),
                ("flat_model", "ascending"),
                ("lease_commence_date", "ascending"),
                ("floor_area_sqm", "ascending"),
                ("month", "ascending"),
                ("street_name", "ascending"),
                ("remaining_lease", "ascending"),
                ("block", "ascending"),
                ("resale_price", "ascending"),
            ]
        )
    )
    f_hdb = BytesIO()
    pq.write_table(merged_hdb_table, f_hdb, compression="ZSTD", compression_level=22)
    f_hdb.seek(0)
    res_hdb = upload_file_to_supabase(
        get_supabase_configs(),
        "sg-housing-db",
        "merged_hdb_resale.parquet.zstd",
        f_hdb,
        upsert=True,
    )
    print(res_hdb.content)
