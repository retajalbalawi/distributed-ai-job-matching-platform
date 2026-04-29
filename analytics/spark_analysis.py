import sqlite3
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, trim, col

DB_PATH = "backend/test.db"

spark = SparkSession.builder \
    .appName("Job Market Analysis From Database") \
    .getOrCreate()

# -----------------------------
# Read jobs from SQLite database
# -----------------------------

conn = sqlite3.connect(DB_PATH)

jobs_df_pandas = pd.read_sql_query(
    """
    SELECT 
        id,
        title,
        company,
        location,
        required_skills,
        description
    FROM jobs
    """,
    conn
)

conn.close()

if jobs_df_pandas.empty:
    print("No jobs found in database. Please create jobs using the FastAPI endpoint first.")
    spark.stop()
    exit()

# Convert Pandas DataFrame to Spark DataFrame
df = spark.createDataFrame(jobs_df_pandas)

# -----------------------------
# Skill demand analysis
# -----------------------------

skills_df = df.select(
    explode(
        split(lower(col("required_skills")), ",")
    ).alias("skill")
)

skills_df = skills_df.select(trim(col("skill")).alias("skill"))

skill_counts = skills_df.groupBy("skill").count().orderBy("count", ascending=False)

print("Top demanded skills:")
skill_counts.show()

skill_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "analytics/output/skill_demand"
)

# -----------------------------
# Location demand analysis
# -----------------------------

location_counts = df.groupBy("location").count().orderBy("count", ascending=False)

print("Top locations:")
location_counts.show()

location_counts.coalesce(1).write.mode("overwrite").option("header", True).csv(
    "analytics/output/location_demand"
)

spark.stop()