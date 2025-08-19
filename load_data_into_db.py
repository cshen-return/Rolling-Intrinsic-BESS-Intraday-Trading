import sys
from datetime import datetime, timedelta
import pytz

from db_helper import DatabaseManager

import os
import csv
def load_hist_csv_per_line(folder_path)->dict:
    """
    Recursively read all CSV files in a folder and print their lines.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Reading file: {file_path}")
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    # Skip the first line
                    next(csvfile)
                    i=1
                    # Read the second line as headers
                    header_line = next(csvfile).strip().split(',')
                    reader = csv.DictReader(csvfile, fieldnames=header_line)
                    for line in reader:
                        i=i+1
                        sys.stdout.write(f"\rReading line {i}")
                        sys.stdout.flush()

                        result={}
                        result['executiontime']=datetime.fromisoformat(line['ExecutionTime'].replace("Z", "+00:00")).astimezone(pytz.timezone('Europe/Amsterdam'))
                        result['deliverystart']=datetime.fromisoformat(line['DeliveryStart'].replace("Z", "+00:00")).astimezone(pytz.timezone('Europe/Amsterdam'))
                        result['deliveryend']=datetime.fromisoformat(line['DeliveryEnd'].replace("Z", "+00:00")).astimezone(pytz.timezone('Europe/Amsterdam'))
                        result['price']=float(line['Price'])
                        result['volume']=float(line['Volume'])
                        result['side']=line['Side']
                        result['product']=line['Product']
                        yield result  # Each line is a dict




if __name__ == "__main__":
    # Connection parameters
    DB_NAME = 'intradaydb'
    DB_USER = 'leloq'
    DB_PASSWORD = '123'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    folder_path = "./data/Continuous_Trades-NL-2024"

    with DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) as db:
        db.drop_table("transactions_intraday_nl")
        # insert table, if not exist, create it
        for aTransaction in load_hist_csv_per_line(folder_path):
            db.insert_transactions(aTransaction, "transactions_intraday_nl", drop_existing=False)