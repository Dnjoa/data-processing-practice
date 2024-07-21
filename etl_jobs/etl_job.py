import logging
from data_load import download_and_extract_data
from data_preprocessing import preprocess_data
from data_transform import process_hard_drive_data
from data_publish import export_csv_to_rdb, get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# RDB connection info
user_name = "username"
password = "password"
host = "localhost"
port = "5432"
database_name = "database_name"


def main():
    # Define input and output directories
    raw_data_directory = "../data/raw_data"
    preprocess_data_directory = "../data/preprocessed_data"
    transform_data_directory = "../data/transformed_data"
    #db_connection_string = get_db_connection(user_name, password, host, port, database_name)

    # Step 1: Download and extract data
    logging.info("Step 1: Downloading and extracting data...")
    download_and_extract_data(raw_data_directory)

    # Step 2: Preprocess data
    logging.info("Step 2: Preprocessing data...")
    preprocess_data(raw_data_directory, preprocess_data_directory)

    # Step 3: Transform data
    logging.info("Step 3: Transforming data...")
    process_hard_drive_data(preprocess_data_directory, transform_data_directory)

    # Step 4: Publish data to RDB
    #logging.info("Step 4: Publishing data to RDB...")
    #export_csv_to_rdb(transform_data_directory, db_connection_string)
    
if __name__ == "__main__":
    main()