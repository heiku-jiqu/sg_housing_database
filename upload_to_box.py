from boxsdk import Client, CCGAuth, OAuth2
from typing import Dict
import json


def get_box_credentials() -> Dict:
    with open("config/keys.json") as f:
        config = json.load(f)["box"]
    return config


def get_sg_housing_db_folder() -> int:
    with open("config/keys.json") as f:
        folder_id = json.load(f)["box_folder_id"]["sg_housing_db"]
    return int(folder_id)


if __name__ == "__main__":
    creds = get_box_credentials()
    print(creds)
    # auth = CCGAuth(
    # client_id="uk600928b7cea5bm81utds9unkpcjtrm",
    # client_secret="4WwbMoKPyY0gXLRLc8B6KLYiFTwmxpQY",
    # user="773326099",
    # )
    auth = OAuth2(
        client_id="riif92ezv5nayueu7c5dynmlyqneb3az",
        access_token="riif92ezv5nayueu7c5dynmlyqneb3az",
    )
    print(auth.access_token)
    client = Client(auth)
    folder = client.folder(get_sg_housing_db_folder())
    file_path = "raw_data/resale_hdb/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.parquet.zstd"
    folder.upload(file_path)
    print(f"File uploaded: {file_path}")
