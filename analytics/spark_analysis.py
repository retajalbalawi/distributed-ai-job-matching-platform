from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, trim

spark = SparkSession.builder \
    .appName("Job Market Analysis") \
    .getOrCreate()

# Sample job data (later you can connect DB)
data = [
    ("AI Engineer Intern", "python, machine learning, deep learning", "Riyadh"),
    ("Data Analyst", "sql, excel, power bi", "Jeddah"),
]

columns = ["title", "skills", "location"]

df = spark.createDataFrame(data, columns)

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

# Location analysis
location_counts = df.groupBy("location").count().orderBy("count", ascending=False)

print("Top locations:")
location_counts.show()

spark.stop()