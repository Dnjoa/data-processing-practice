from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col, year
import glob

def process_hard_drive_data(input_dir, output_dir):
    spark = SparkSession.builder.appName("HardDriveDataProcessing").getOrCreate()

    # Read all CSV files into a single DataFrame
    files = glob.glob(f"{input_dir}/*.csv")
    df = spark.read.csv(files, header=True, inferSchema=True)

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
