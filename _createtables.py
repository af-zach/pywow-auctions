import os
from psql import PostgreSQL

# Create database connection
psql = PostgreSQL('localhost', 'wow_data', os.environ.get('PSQL_USER'), os.environ.get('PSQL_PASS'))
cur = psql.conn.cursor()

# Remove tables if they exist
cur.execute("DROP TABLE IF EXISTS realms, auctions")
psql.conn.commit()

realms = '''CREATE TABLE realms (
    realm_id smallint,
    name VARCHAR NOT NULL,
    population VARCHAR NOT NULL,
    region VARCHAR NOT NULL,
    timezone VARCHAR NOT NULL,
    locale VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    slug VARCHAR NOT NULL,
    auctions_last_modified VARCHAR,
    last_modified VARCHAR NOT NULL,
    created_at VARCHAR NOT NULL,
    PRIMARY KEY (realm_id)
);'''

auctions = '''CREATE TABLE auctions (
    auction_id bigint,
    realm_id smallint NOT NULL,
    item_id bigint NOT NULL,
    quantity bigint NOT NULL,
    buyout bigint NOT NULL,
    auction_duration VARCHAR,
    wow_version int NOT NULL,
    last_modified VARCHAR NOT NULL,
    created_at VARCHAR NOT NULL,
    PRIMARY KEY (auction_id),
    FOREIGN KEY (realm_id) REFERENCES realms(realm_id) ON DELETE CASCADE
);'''

cur.execute(realms)
cur.execute(auctions)
psql.conn.commit()
psql.close_connection()