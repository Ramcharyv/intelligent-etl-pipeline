from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master('local') \
    .appName('test') \
    .config('spark.jars.packages', 'io.delta:delta-core_2.12:2.4.0') \
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
    .getOrCreate()

spark.createDataFrame([('ok',)], ['status']).show()
spark.stop()
print('Spark OK')
