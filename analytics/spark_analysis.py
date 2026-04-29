from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, trim

spark = SparkSession.builder \
    .appName("Job Market Analysis") \
    .getOrCreate()

df = spark.read.csv(
    "data/jobs/sample_jobs.csv",
    header=True,
    inferSchema=True
)

# Split skills into rows
skills_df = df.select(
    explode(
        split(lower(df.skills), ",")
    ).alias("skill")
)

# Clean whitespace
skills_df = skills_df.select(trim(skills_df.skill).alias("skill"))

# Count skills
skill_counts = skills_df.groupBy("skill").count().orderBy("count", ascending=False)

print("Top demanded skills:")
skill_counts.show()

skill_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "analytics/output/skill_demand"
)

# Location analysis
location_counts = df.groupBy("location").count().orderBy("count", ascending=False)

print("Top locations:")
location_counts.show()

location_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "analytics/output/location_demand"
)

spark.stop()