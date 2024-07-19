from pyspark.sql import SparkSession

def preprocess_data(input_directory, output_directory):
    # Initialize Spark Session
    spark = SparkSession.builder.appName("Data Preprocessing").getOrCreate()

    # Read all CSV files from the input directory
    df = spark.read.option("header", "true").csv(f"{input_directory}/*.csv")

    # Extract specific columns
    selected_columns_df = df.select("date", "model", "failure")

    # Save the processed DataFrame to a new CSV file in the output directory
    selected_columns_df.write.option("header", "true").csv(f"{output_directory}/processed_data", mode="overwrite")

    # Stop the Spark session
    spark.stop()