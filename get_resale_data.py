import requests
from pprint import pprint
import pandas as pd

resource_id = {
    '2017 onwards': 'f1765b54-a209-4718-8d38-a39237f502b3',
    'Jan 2015 - Dec 2016': '1b702208-44bf-4829-b620-4615ee19b57c',
    'Mar 2012 - Dec 2014': '83b2fc37-ce8c-4df4-968b-370fd818138b',
    '2000 - Feb 2012': '8c00bf08-9124-479e-aeca-7cc411d884c4',
    '1990 - 1999': 'adbbddd3-30e2-445f-a123-29bee150a6fe'
}
params = {
    'resource_id': resource_id['2017 onwards'],
    'limit': 100
}
response = requests.get(
    url = 'https://data.gov.sg/api/action/datastore_search',
    params = params
)

# pprint(response.json()['result']['records'])

rows = response.json()['result']['records']

df = pd.DataFrame(rows)
df.to_csv('data1.csv')
# df.to_parquet('data.parquet')
# df.to_feather('data.feather')