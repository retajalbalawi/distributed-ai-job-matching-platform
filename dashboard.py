import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Job Market Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Job Market Analytics Dashboard")

st.markdown(
    """
    This dashboard analyzes job-market trends from the PySpark analytics pipeline.
    It highlights in-demand technical skills, hiring locations, and key insights
    to help graduates understand where to focus their learning.
    """
)

SKILL_PATH = "analytics/output/skill_demand"
LOCATION_PATH = "analytics/output/location_demand"


def load_csv_from_folder(folder_path):
    if not os.path.exists(folder_path):
        return None

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            return pd.read_csv(os.path.join(folder_path, file))

    return None


skills_df = load_csv_from_folder(SKILL_PATH)
locations_df = load_csv_from_folder(LOCATION_PATH)

if skills_df is None or locations_df is None:
    st.error("Analytics output files were not found. Please run the PySpark analysis first.")
    st.code(
        """
export PYSPARK_PYTHON=/opt/anaconda3/bin/python
export PYSPARK_DRIVER_PYTHON=/opt/anaconda3/bin/python
python analytics/spark_analysis.py
        """
    )
    st.stop()

skills_df = skills_df.sort_values("count", ascending=False)
locations_df = locations_df.sort_values("count", ascending=False)

top_skill = skills_df.iloc[0]["skill"]
top_skill_count = int(skills_df.iloc[0]["count"])
top_location = locations_df.iloc[0]["location"]
top_location_count = int(locations_df.iloc[0]["count"])

# -----------------------------
# KPI Metrics
# -----------------------------

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Unique Skills", skills_df["skill"].nunique())

with col2:
    st.metric("Total Skill Mentions", int(skills_df["count"].sum()))

with col3:
    st.metric("Hiring Locations", locations_df["location"].nunique())

with col4:
    st.metric("Top Skill Mentions", top_skill_count)

st.success(f"🔥 Most demanded skill: {top_skill.title()}")
st.info(f"📍 Strongest hiring location: {top_location} ({top_location_count} job mention(s))")

st.divider()

# -----------------------------
# Filters
# -----------------------------

st.sidebar.header("Dashboard Controls")

top_n_skills = st.sidebar.slider(
    "Number of top skills to display",
    min_value=3,
    max_value=max(3, min(20, len(skills_df))),
    value=min(10, len(skills_df)),
)

top_n_locations = st.sidebar.slider(
    "Number of top locations to display",
    min_value=1,
    max_value=max(1, min(20, len(locations_df))),
    value=min(10, len(locations_df)),
)

# -----------------------------
# Charts
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top In-Demand Skills")
    top_skills_chart = (
        skills_df.head(top_n_skills)
        .sort_values("count", ascending=True)
        .set_index("skill")["count"]
    )
    st.bar_chart(top_skills_chart)

with col2:
    st.subheader("Top Hiring Locations")
    top_locations_chart = (
        locations_df.head(top_n_locations)
        .sort_values("count", ascending=True)
        .set_index("location")["count"]
    )
    st.bar_chart(top_locations_chart)

st.divider()

# -----------------------------
# Tables
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Skill Demand Table")
    st.dataframe(
        skills_df.head(top_n_skills),
        use_container_width=True,
        hide_index=True,
    )

with col2:
    st.subheader("Location Demand Table")
    st.dataframe(
        locations_df.head(top_n_locations),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# -----------------------------
# Insights
# -----------------------------

st.subheader("Key Insights")

st.markdown(
    f"""
    - **{top_skill.title()}** appears as the most demanded skill in the current dataset.
    - **{top_location}** appears as the strongest hiring location in the current dataset.
    - The dashboard is powered by a **PySpark analytics pipeline** that processes job descriptions and aggregates market trends.
    - These insights help graduates identify which technical skills to prioritize before applying to jobs.
    """
)

st.warning(
    "Current dataset is small. For stronger insights, connect a larger real-world job dataset."
)