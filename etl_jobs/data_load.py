import io
import logging
import requests
import zipfile
import pandas as pd
import os
from config.url_config import get_url_list

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_and_extract_data(folder_prefix):
    url_list = get_url_list(folder_prefix)
    logging.info(f"Downloading and extracting data from {len(url_list)} URLs...")
    for item in url_list:
        url = item['url']
        folder = item['folder']
        
        # Create the folder if it doesn't exist, if exist do nothing and break
        if os.path.exists(folder):
            logging.info(f"Folder {folder} already exists.")
            break
        else:
            os.makedirs(folder)
            logging.info(f"Folder {folder} created.")
        
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        file_path = os.path.join(folder, filename)
        
        logging.info(f"Starting download of {url} into {file_path}")
        
        # Download the ZIP file
        response = requests.get(url)
        logging.info(f"Already download the ZIP file")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the ZIP file locally
            # with open(file_path, 'wb') as file:
            #    file.write(response.content)
            
            # Use BytesIO to create a file-like object from the content of the response
            zip_in_memory = io.BytesIO(response.content)
            
            # Extract the ZIP file
            extract_zip_without_macosx(zip_in_memory, folder)
            
            # Read one file of the extracted files
            for file in os.listdir(folder):
                if file.endswith(".csv"):
                    file_path = os.path.join(folder, file)
                    df = pd.read_csv(file_path)
                    logging.info(f"Read {len(df)} rows from {file_path}")
                    # Display the first few rows of the DataFrame
                    print(df.head())
                    break
        else:
            print(f"Failed to download {filename}: {response.status_code}")
            
    logging.info("Data download and extraction complete.")


def extract_zip_without_macosx(zip_in_memory, extract_to):
    with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
        # List all the file names in the zip and filter out any path segment containing _MACOSX
        valid_files = [item for item in zip_ref.namelist() if '__MACOSX' not in item.split('/')]
        # Extract only the filtered files
        for file in valid_files:
            zip_ref.extract(file, extract_to)