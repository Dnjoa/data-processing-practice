import logging
import pandas as pd

from etl_jobs.config.db_connection_config import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_csv_to_rdb(input_dir, db_connection_string):
    # Get database connection
    engine = get_db_connection()
    logging.info("Connected to the database.")

    # Read CSV files
    hard_drive_by_date_df = pd.read_csv(f"{input_dir}/hard_drive_by_date.csv")
    hard_drive_by_year_df = pd.read_csv(f"{input_dir}/hard_drive_by_year.csv")

    # Export DataFrames to RDB
    export_df_to_rdb(hard_drive_by_date_df, 'hard_drive_by_date', engine)
    logging.info("Exported hard_drive_by_date DataFrame to the database.")
    
    export_df_to_rdb(hard_drive_by_year_df, 'hard_drive_by_year', engine)
    logging.info("Exported hard_drive_by_year DataFrame to the database.")

def export_df_to_rdb(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
