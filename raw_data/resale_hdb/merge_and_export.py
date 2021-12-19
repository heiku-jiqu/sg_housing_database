# merge all csv files and export to loading_area directory

import pandas as pd
import glob
import os

directory = r"raw_data\resale_hdb"

csv_files_in_directory = glob.glob(os.path.join(directory,"*.csv"))

df_from_each_file = (pd.read_csv(f) for f in csv_files_in_directory)

concatenated_df = (pd.concat(df_from_each_file)
    .sort_values(by='month', ignore_index=True)
)
concatenated_df['remaining_lease'] = concatenated_df['remaining_lease'].fillna("").astype(str)
concatenated_df['flat_type'] = concatenated_df['flat_type'].replace('MULTI-GENERATION', 'MULTI GENERATION')
concatenated_df['flat_model'] = concatenated_df['flat_model'].str.upper()

concatenated_df.to_csv("loading_area/resale_hdb/resale_hdb.csv", index = False)
concatenated_df.to_parquet("loading_area/resale_hdb/resale_hdb.parquet")