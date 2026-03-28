import streamlit as st
import pandas as pd
import os

def show_analytics():

    file_path = "data/audio/performance.csv"

    st.header("📊 Learning Analytics Dashboard")

    # Check if file exists
    if not os.path.exists(file_path):
        st.warning("No performance data available yet.")
        return

    df = pd.read_csv(file_path)

    # Check if dataframe is empty
    if df.empty:
        st.warning("No performance data available yet.")
        return

    # Ensure required columns exist
    required_columns = {"topic", "correct", "type", "date"}
    if not required_columns.issubset(df.columns):
        st.error("Performance data format is incorrect.")
        return

    # Accuracy Over Time
    st.subheader("📈 Accuracy Over Time")
    accuracy = df.groupby("date")["correct"].mean()
    st.line_chart(accuracy)

    # Topic Mastery
    st.subheader("📊 Topic Mastery")
    topic_accuracy = df.groupby("topic")["correct"].mean()
    st.bar_chart(topic_accuracy)

    # Daily Study Activity
    st.subheader("📅 Daily Study Activity")
    activity = df.groupby("date").size()
    st.bar_chart(activity)

    # Overall Mastery
    st.subheader("🎯 Overall Knowledge Mastery")
    mastery = df["correct"].mean() * 100
    st.metric("Mastery Score", f"{mastery:.2f}%")