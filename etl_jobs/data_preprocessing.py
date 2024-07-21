import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, date_format

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(input_directory, output_directory):
    # Set SPARK_HOME environment variable
    # os.environ['SPARK_HOME'] = '/myenv/lib/python3.12/site-packages'
    
    logging.info(f"Preprocessing data from {input_directory} and saving the results to {output_directory}...")
    
    # Initialize Spark Session
    spark = SparkSession.builder.appName("Data Preprocessing").getOrCreate()

    # Read all CSV files from the input directory
    df = spark.read.option("header", "true").csv(f"{input_directory}/*.csv")

    # Extract specific columns
    selected_columns_df = df.select("date", "model", "failure")
    logging.info(f"Selected {len(selected_columns_df.columns)} columns: {selected_columns_df.columns}")
    
    # Perform data cleaning and transformation
    altered_columns_df = selected_columns_df.withColumn(
        "model",
        when(col("model").startswith("CT"), "Crucial")
        .when(col("model").startswith("DELLBOSS"), "Dell BOSS")
        .when(col("model").startswith("HGST"), "HGST")
        .when(col("model").startswith("Seagate") | col("model").startswith("ST"), "Seagate")
        .when(col("model").startswith("TOSHIBA"), "Toshiba")
        .when(col("model").startswith("WDC"), "Western Digital")
        .otherwise("Others")
    ).withColumn(
        "failure",
        when(col("failure") == "1", "Yes")
        .when(col("failure") == "0", "No")
        .otherwise("Unknown")
    ).withColumn(
        "date",
        when(col("date").contains("/"), date_format(col("date"), "yyyy-MM-dd"))
    )
    logging.info("Data cleaning and transformation complete.")
    
    # Create the output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Save the processed DataFrame to a new CSV file in the output directory
    altered_columns_df.write.option("header", "true").csv(f"{output_directory}", mode="overwrite")
    logging.info("Saved the processed data to a new CSV file.")

    # Stop the Spark session
    spark.stop()