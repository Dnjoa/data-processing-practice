from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("PySpark Test") \
    .getOrCreate()

# Create a DataFrame
data = [("John Doe", 30), ("Jane Doe", 25)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, schema=columns)

# Show the DataFrame
df.show()

# Stop the SparkSession
spark.stop()