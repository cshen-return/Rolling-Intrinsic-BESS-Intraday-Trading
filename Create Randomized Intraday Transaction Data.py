# %%
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random
import pytz

# %%


# Set the Europe/Berlin timezone
berlin_tz = pytz.timezone('Europe/Berlin')

# Connection parameters
db_name = 'intradaydb'
db_user = 'leloq'
db_password = '123'
db_host = 'localhost'
db_port = '5432'

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Create a cursor object
cur = conn.cursor()

# SQL to drop the table if it exists and create a new one
create_table_query = """
DROP TABLE IF EXISTS transactions_intraday_de;

CREATE TABLE IF NOT EXISTS transactions_intraday_de (
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

# Execute the SQL to drop and create the table
try:
    cur.execute(create_table_query)
    conn.commit()
    print("Table 'transactions_intraday_de' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")

# Function to round datetime object to the nearest full hour
def round_to_full_hour(dt):
    # If the minutes are 30 or more, round up to the next hour
    if dt.minute >= 30:
        dt = dt + timedelta(hours=1)
    
    # Set minutes, seconds, and microseconds to zero
    return dt.replace(minute=0, second=0, microsecond=0)

# Function to generate a random timezone-aware timestamp in 2022, rounded to the nearest full hour
def random_time_in_2022():
    start = berlin_tz.localize(datetime(2022, 1, 1))  # Timezone-aware datetime
    end = berlin_tz.localize(datetime(2023, 1, 2, 23, 59, 59))  # Full year 2022

    # Calculate the total number of hours between start and end
    total_hours = int((end - start).total_seconds() // 3600)

    # Generate a random number of hours
    random_hours = random.randint(0, total_hours)

    # Add the random number of hours to the start date
    random_time = start + timedelta(hours=random_hours)

    # Round to the nearest full hour
    return round_to_full_hour(random_time)

# Function to generate a deliverystart within the next 16 hours, ensuring deliverystart is a full hour
def random_deliverystart(executiontime):
    # Round the execution time to the nearest full hour (if needed)
    rounded_executiontime = round_to_full_hour(executiontime)
    
    # Add a random number of full hours between 0 and 15 (inclusive)
    random_hours = random.randint(0, 15)
    
    # Calculate deliverystart, which will always be at a full hour
    deliverystart = rounded_executiontime + timedelta(hours=random_hours)
    
    # Ensure deliverystart is rounded to the full hour
    return round_to_full_hour(deliverystart)

# Generate and insert fake transactions into the transactions_intraday_de table
def insert_fake_transactions(num_transactions=100):
    count = 0
    while count < num_transactions:
        # Generate the base execution time, timezone-aware and rounded to full hour
        base_executiontime = random_time_in_2022()

        # Insert the first transaction with the base execution time
        for i in range(6):  # Insert the base transaction + 5 more transactions within the next 5 minutes
            if i == 0:
                executiontime = base_executiontime
            else:
                # Add a random number of minutes and round the executiontime to the nearest minute
                executiontime = (base_executiontime + timedelta(minutes=i)).replace(second=0, microsecond=0)

            # Ensure executiontime is rounded to a full hour
            executiontime = round_to_full_hour(executiontime)

            # Set deliverystart to be within the next 16 hours and ensure it's on a full hour
            deliverystart = random_deliverystart(executiontime)
            deliveryend = deliverystart + timedelta(minutes=60)

            price = round(random.uniform(20, 100), 2)  # Random price between 20 and 100
            volume = round(random.uniform(1, 10), 2)  # Random volume between 1 and 10
            side = random.choice(['BUY', 'SELL'])  # Randomly choose 'buy' or 'sell'
            product = random.choice(['XBID_Hour_Power', 'Intraday_Hour_Power'])  # Randomly choose the product

            # Insert the transaction into the transactions_intraday_de table
            cur.execute(
                sql.SQL("INSERT INTO transactions_intraday_de (executiontime, deliverystart, deliveryend, price, volume, side, product) VALUES (%s, %s, %s, %s, %s, %s, %s);"),
                [executiontime, deliverystart, deliveryend, price, volume, side, product]
            )
            count += 1

    # Commit the transaction
    conn.commit()
    print(f"{num_transactions} fake transactions inserted successfully!")


# Insert 1,000,000 fake transactions
insert_fake_transactions(1_000_000)

# Close the cursor and connection
cur.close()
conn.close()


# %%


# Set the Europe/Berlin timezone
berlin_tz = pytz.timezone('Europe/Berlin')

# Connection parameters
db_name = 'intradaydb'
db_user = 'leloq'
db_password = '123'
db_host = 'localhost'
db_port = '5432'

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Create a cursor object
cur = conn.cursor()

# SQL to drop the table if it exists and create a new one
create_table_query = """
CREATE TABLE IF NOT EXISTS transactions_intraday_de (
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

# Execute the SQL to drop and create the table
try:
    cur.execute(create_table_query)
    conn.commit()
    print("Table 'transactions_intraday_de' created successfully!")
except Exception as e:
    print(f"Error creating table: {e}")

# Function to round datetime object to the nearest full hour
def round_to_full_hour(dt):
    # If the minutes are 30 or more, round up to the next hour
    if dt.minute >= 30:
        dt = dt + timedelta(hours=1)
    
    # Set minutes, seconds, and microseconds to zero
    return dt.replace(minute=random.choice([0,15,30,45]), second=0, microsecond=0)

# Function to generate a random timezone-aware timestamp in 2022, rounded to the nearest full hour
def random_time_in_2022():
    start = berlin_tz.localize(datetime(2022, 1, 1))  # Timezone-aware datetime
    end = berlin_tz.localize(datetime(2023, 1, 1, 23, 59, 59))  # Full year 2022

    # Calculate the total number of hours between start and end
    total_hours = int((end - start).total_seconds() // 3600)

    # Generate a random number of hours
    random_hours = random.randint(0, total_hours)

    # Add the random number of hours to the start date
    random_time = start + timedelta(hours=random_hours)

    # Round to the nearest full hour
    return round_to_full_hour(random_time)

# Function to generate a deliverystart within the next 16 hours, ensuring deliverystart is a full hour
def random_deliverystart(executiontime):
    # Round the execution time to the nearest full hour (if needed)
    rounded_executiontime = round_to_full_hour(executiontime)
    
    # Add a random number of full hours between 0 and 15 (inclusive)
    random_hours = random.randint(0, 15)
    
    # Calculate deliverystart, which will always be at a full hour
    deliverystart = rounded_executiontime + timedelta(hours=random_hours)
    
    # Ensure deliverystart is rounded to the full hour
    return round_to_full_hour(deliverystart)

# Generate and insert fake transactions into the transactions_intraday_de table
def insert_fake_transactions(num_transactions=100):
    count = 0
    while count < num_transactions:
        # Generate the base execution time, timezone-aware and rounded to full hour
        base_executiontime = random_time_in_2022()

        # Insert the first transaction with the base execution time
        for i in range(6):  # Insert the base transaction + 5 more transactions within the next 5 minutes
            if i == 0:
                executiontime = base_executiontime
            else:
                # Add a random number of minutes and round the executiontime to the nearest minute
                executiontime = (base_executiontime + timedelta(minutes=i)).replace(second=0, microsecond=0)

            # Ensure executiontime is rounded to a full hour
            executiontime = round_to_full_hour(executiontime)

            # Set deliverystart to be within the next 16 hours and ensure it's on a full hour
            deliverystart = random_deliverystart(executiontime)
            deliveryend = deliverystart + timedelta(minutes=15)

            price = round(random.uniform(20, 100), 2)  # Random price between 20 and 100
            volume = round(random.uniform(1, 10), 2)  # Random volume between 1 and 10
            side = random.choice(['BUY', 'SELL'])  # Randomly choose 'buy' or 'sell'
            product = random.choice(['XBID_Quarter_Hour_Power', 'Intraday_Quarter_Hour_Power'])  # Randomly choose the product

            # Insert the transaction into the transactions_intraday_de table
            cur.execute(
                sql.SQL("INSERT INTO transactions_intraday_de (executiontime, deliverystart, deliveryend, price, volume, side, product) VALUES (%s, %s, %s, %s, %s, %s, %s);"),
                [executiontime, deliverystart, deliveryend, price, volume, side, product]
            )
            count += 1

    # Commit the transaction
    conn.commit()
    print(f"{num_transactions} fake transactions inserted successfully!")


# Insert 1,000,000 fake transactions
insert_fake_transactions(1_000_000)

# Close the cursor and connection
cur.close()
conn.close()


# %%


# %%


# %%



