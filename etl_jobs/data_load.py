import requests
import zipfile
import pandas as pd
import os
from url_config import get_url_list

def download_and_extract_data(folder_prefix):
    url_list = get_url_list(folder_prefix)
    for item in url_list:
        url = item['url']
        folder = item['folder']
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        file_path = os.path.join(folder, filename)
        
        # Download the ZIP file
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the ZIP file locally
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            # Extract the ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder)
            
            # Iterate through the extracted files
            for filename in os.listdir(folder):
                if filename.endswith('.csv'):
                    # Construct the full path to the file
                    csv_file_path = os.path.join(folder, filename)
                    # Read the CSV file
                    df = pd.read_csv(csv_file_path)
                    # Process the data (example: print the DataFrame)
                    print(f"Data from {filename}:")
                    print(df.head())  # Display the first few rows of the DataFrame
        else:
            print(f"Failed to download {filename}: {response.status_code}")
