import logging
import os
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col, year
import glob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_hard_drive_data(input_dir, output_dir):
    logging.info(f"Processing hard drive data from {input_dir} and saving the results to {output_dir}...")
    spark = SparkSession.builder.appName("HardDriveDataProcessing").getOrCreate()

    # Read all CSV files into a single DataFrame
    files = glob.glob(f"{input_dir}/*.csv")
    df = spark.read.csv(files, header=True, inferSchema=True)
    logging.info("Read all CSV files into a single DataFrame.")
    
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Hard Drive by Date Table
    hard_drive_by_date = df.groupBy("date").agg(
        F.count("*").alias("count"),
        F.sum(
            F.when(
                col("failure").eqNullSafe("Yes"), 1
                ).otherwise(0)
            ).alias("failure_count")
    )
    hard_drive_by_date.write.csv(f"{output_dir}/hard_drive_by_date.csv", header=True, mode="overwrite")
    logging.info("Calaulate the failed count by date and saved into Date Table.")

    # Hard Drive by Year Table
    hard_drive_by_year = df.withColumn(
        "year", year("date")
        ).groupBy("year", "model").agg(
        F.sum(
            F.when(
                col("failure").eqNullSafe("Yes"), 1).otherwise(0)
            ).alias("failure_count")
    ).withColumnRenamed("model", "brand")
    hard_drive_by_year.write.csv(f"{output_dir}/hard_drive_by_year.csv", header=True, mode="overwrite")
    logging.info("Calaulate the failed count by year and saved into Year Table.")
