from datetime import datetime, timedelta

import psycopg2
import pytz

# SQL for table creation
# no 'f' because the string is a tempalte and the 'table_name' will be changed in .format()
CREATE_TABLE_SQL = """
    DROP TABLE IF EXISTS {table_name};

    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        executiontime TIMESTAMP WITH TIME ZONE NOT NULL,
        deliverystart TIMESTAMP WITH TIME ZONE NOT NULL,
        deliveryend TIMESTAMP WITH TIME ZONE NOT NULL,
        price REAL NOT NULL,
        volume REAL NOT NULL,
        side VARCHAR(4) NOT NULL,
        product VARCHAR(50) NOT NULL
    );
    """

# SQL for inserting
INSERT_DATA_SQL = """
    INSERT INTO {table_name} 
    (executiontime, deliverystart, deliveryend, price, volume, side, product)
    VALUES (%(executiontime)s, %(deliverystart)s, %(deliveryend)s, %(price)s, %(volume)s, %(side)s, %(product)s);
    """

# SQL for checking if the table exist
CHECK_TABLE_EXISTS_SQL = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = '{table_name}'
    );
    """

# SQL for delete table
DROP_TABLE_SQL = """
    DROP TABLE IF EXISTS {table_name};  
    """



class DatabaseManager:

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
        self.table_name="transactions_intraday_de"




    def __enter__(self):
        """Open connection and cursor when entering context."""
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()
        return self  # return the instance itself so we can use its methods

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure cleanup on exit (even if error happens)."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query_template, table_name, params=None, commit=False, drop_table=False):
        """
        Executes a SQL query with optional parameters.
        If commit=True, commits the transaction.

        If drop_table=True and table_name provided:
            - If table exists -> drop it
            - If table does not exist -> create it using `query`
        """
        try:
            # Replace placeholder with actual table name
            query = query_template.format(table_name=table_name)

            # Check if table exists
            self.cur.execute(CHECK_TABLE_EXISTS_SQL.format(table_name=table_name))
            exists = self.cur.fetchone()[0]

            #if need to drop
            if exists and drop_table:
                # drop the table
                self.cur.execute(DROP_TABLE_SQL.format(table_name=table_name))
                print(f"Table '{table_name}' dropped (cleaned).")
                exists=False

            # if not exist
            if not exists:
                # Create table with provided SQL
                self.cur.execute(CREATE_TABLE_SQL.format(table_name=table_name))
                print(f"Table '{table_name}' created.")

            # Normal query execution
            self.cur.execute(query, params)
            if commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error executing query: {e}")
            raise

    def insert_transactions(self,transactions,table_name="transactions_intraday_de",drop_existing=False):
        self.execute_query(INSERT_DATA_SQL,table_name,transactions,commit=True,drop_table=drop_existing)

    def drop_table(self,table_name="transactions_intraday_de"):
        self.execute_query(DROP_TABLE_SQL,table_name,drop_table=True)

if __name__ == "__main__":
    # Connection parameters
    DB_NAME = 'intradaydb'
    DB_USER = 'leloq'
    DB_PASSWORD = '123'
    DB_HOST = 'localhost'
    DB_PORT = '5432'

    with DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD,DB_HOST,DB_PORT) as db:
        now = datetime.now(pytz.timezone('Europe/Amsterdam'))
        transactions = {
            "executiontime": now,
            "deliverystart": now,
            "deliveryend": now + timedelta(hours=1),
            "price": 150.75,
            "volume": 20,
            "side": "BUY",
            "product": "TestProduct"
        }

        # insert table, if not exist, create it
        db.insert_transactions(transactions,"transactions_intraday_nl",drop_existing=True)

