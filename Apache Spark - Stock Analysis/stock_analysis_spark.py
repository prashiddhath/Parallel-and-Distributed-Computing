
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Stock Analysis").getOrCreate()

mySchema = StructType([
    StructField("date", StringType(), False),
    StructField("appl_open", FloatType(), False),
    StructField("ibm_open", FloatType(), False),
])

df = spark.read.format("csv").option("header", "true").schema(mySchema).load('APPL_IBM_open.csv')

result = df.select(expr("substring(date,1,4) as year"), expr("substring(date,6,2) as month"), expr("appl_open"), expr("ibm_open")).filter(col("month").isin["10", "11", "12"]).groupBy("year").agg(max("appl_open"), max("ibm_open"))

result.write.format("csv").option("path", "output").save()
