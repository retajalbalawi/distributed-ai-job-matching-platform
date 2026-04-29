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
    It highlights the most demanded skills and top hiring locations for tech-related roles.
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

# -----------------------------
# KPI Metrics
# -----------------------------

st.subheader("Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unique Skills", skills_df["skill"].nunique())

with col2:
    st.metric("Total Skill Mentions", int(skills_df["count"].sum()))

with col3:
    st.metric("Hiring Locations", locations_df["location"].nunique())

st.divider()

# -----------------------------
# Filters
# -----------------------------

st.sidebar.header("Dashboard Controls")

top_n_skills = st.sidebar.slider(
    "Number of top skills to display",
    min_value=3,
    max_value=min(20, len(skills_df)),
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
    st.bar_chart(
        skills_df.head(top_n_skills).set_index("skill")["count"]
    )

with col2:
    st.subheader("Top Hiring Locations")
    st.bar_chart(
        locations_df.head(top_n_locations).set_index("location")["count"]
    )

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

top_skill = skills_df.iloc[0]["skill"]
top_location = locations_df.iloc[0]["location"]

st.markdown(
    f"""
    - **{top_skill.title()}** appears as the most demanded skill in the current dataset.
    - **{top_location}** appears as the strongest hiring location in the current dataset.
    - The dashboard is powered by a PySpark pipeline that processes job descriptions and aggregates market trends.
    - These insights can help graduates identify which technical skills to prioritize.
    """
)

st.info(
    "Next improvement: connect this dashboard to a larger real-world job dataset for stronger market insights."
)