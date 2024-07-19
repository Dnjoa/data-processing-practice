from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, date_format

def preprocess_data(input_directory, output_directory):
    # Initialize Spark Session
    spark = SparkSession.builder.appName("Data Preprocessing").getOrCreate()

    # Read all CSV files from the input directory
    df = spark.read.option("header", "true").csv(f"{input_directory}/*.csv")

    # Extract specific columns
    selected_columns_df = df.select("date", "model", "failure")
    
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
    
    # Save the processed DataFrame to a new CSV file in the output directory
    altered_columns_df.write.option("header", "true").csv(f"{output_directory}/processed_data", mode="overwrite")

    # Stop the Spark session
    spark.stop()