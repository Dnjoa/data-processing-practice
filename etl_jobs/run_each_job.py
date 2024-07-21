from data_load import download_and_extract_data
from data_preprocessing import preprocess_data

download_and_extract_data("../data/raw_data")
preprocess_data("../data/raw_data", "../data/preprocessed_data")