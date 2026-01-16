import pandas as pd
from sqlalchemy import create_engine
import os

conn_string = "postgresql://analyst:password123@localhost:5432/olist_ecommerce"
engine = create_engine(conn_string)

def load_csv_to_postgres(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            table_name = file.replace("olist_", "").replace("_dataset", "").replace(".csv", "")
            file_path = os.path.join(folder_path, file)

            print(f"Loading {file} in '{table_name}'...")

            df = pd.read_csv(file_path)

            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Table {table_name} created")

if __name__ == "__main__":
    data_folder = "./data/"
    load_csv_to_postgres(data_folder)