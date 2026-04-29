import pandas as pd
import streamlit as st
import os

st.title("📊 Job Market Analytics Dashboard")

# Load data
skill_path = "analytics/output/skill_demand"
location_path = "analytics/output/location_demand"

def load_csv(folder):
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            return pd.read_csv(os.path.join(folder, file))
    return None

skills_df = load_csv(skill_path)
locations_df = load_csv(location_path)

if skills_df is not None:
    st.subheader("Top Skills")
    st.bar_chart(skills_df.set_index("skill"))

if locations_df is not None:
    st.subheader("Top Locations")
    st.bar_chart(locations_df.set_index("location"))