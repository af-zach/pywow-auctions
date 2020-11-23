import psycopg2
import psycopg2.extras

class PostgreSQL():
    def __init__(self, dbhost, dbname, user, password):
        self.dbhost = dbhost
        self.dbname = dbname
        self.user = user
        self.password = password

        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.dbhost)

    def close_connection(self):
        self.conn.close()

    # Function to get realm_id and auction_last_modified columns for all realms in realms table
    def get_realms_table(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"SELECT realm_id, auction_last_modified FROM realms")
            result = cur.fetchall()
            realms = []
            for row in result:
                realms.append(dict(row))
        return realms

    # Retrieve all data for a single realm by realm_id
    def get_single_realm(self, realm_id):
        self.realm_id = realm_id
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"SELECT * FROM realms WHERE realm_id = '{self.realm_id}';")
            realm = dict(cur.fetchone())
        return realm

    # Insert new realm into realms table one row at time 
    # EXAMPLE: psql.insert_realm(id="7", name="Area 52")
    def insert_realm(self, **kwargs):
        self.columns = str(tuple(kwargs.keys())).replace("'","")
        self.values = tuple(kwargs.values())
        with self.conn.cursor() as cur:
            cur.execute(f"INSERT INTO realms {self.columns} VALUES {self.values} ON CONFLICT DO NOTHING;")
            self.conn.commit()