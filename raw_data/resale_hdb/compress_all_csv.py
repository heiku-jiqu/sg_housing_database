import zstandard
import glob

cctx = zstandard.ZstdCompressor()
dctx = zstandard.ZstdDecompressor()
compressed = cctx.compress(b"data to compress")

directory = "raw_data/resale_hdb"

csv_files_in_directory = glob.glob(f"{directory}/*.csv")
zstd_files_to_output = [path.replace(".csv",".zstd") for path in csv_files_in_directory]

for input_path, output_path in zip(csv_files_in_directory, zstd_files_to_output):
    with open(input_path,'rb') as ifh, open(output_path, 'wb') as ofh:
            cctx.copy_stream(ifh, ofh)

# # compress csv file to zstd file
# with open(input_path,'rb') as ifh, open(output_path, 'wb') as ofh:
#         cctx.copy_stream(ifh, ofh)

# # decompress zstd file to csv file
# with open(output_path,'rb') as ifh, open("raw_data/resale_hdb/testing.csv", 'wb') as ofh:
#         dctx.copy_stream(ifh, ofh)

