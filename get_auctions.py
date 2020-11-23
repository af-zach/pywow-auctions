from wowapi import WowApi
from psql import PostgreSQL
import os

pqsl = PostgreSQL('localhost', 'wow_data', os.environ.get('PSQL_USER'), os.environ.get('PSQL_PASS'))
wowapi = WowApi(os.environ.get('WOWAPI_CLIENT'), os.environ.get('WOWAPI_SECRET'))

#temp placeholder for realm id's
realm_id = 3676
last_modified = 1

auctions = wowapi.get_auctions('us', 'dynamic-us', realm_id, locale='en_US')