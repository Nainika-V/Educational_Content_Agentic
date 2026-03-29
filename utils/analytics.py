import streamlit as st
import pandas as pd
import os
import datetime

def save_quiz_result(topic, score, total):
    """
    Saves the quiz performance to a CSV file.
    """
    file_path = "data/audio/performance.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    accuracy = score / total if total > 0 else 0
    date = datetime.date.today().strftime("%Y-%m-%d")
    
    new_data = pd.DataFrame([{
        "topic": topic,
        "correct": accuracy,
        "type": "quiz",
        "date": date
    }])
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df = pd.concat([df, new_data], ignore_index=True)
        except Exception:
            df = new_data
    else:
        df = new_data
        
    df.to_csv(file_path, index=False)

def show_analytics():

    file_path = "data/audio/performance.csv"

    st.header("Learning Analytics Dashboard")

    # Check if a quiz was taken in this session
    if not st.session_state.get("quiz_taken", False):
        st.warning("You haven't taken a quiz yet in this session. Please complete at least one quiz to unlock your learning analytics!")
        return

    # Check if file exists
    if not os.path.exists(file_path):
        st.info("No historical performance data found. Complete more quizzes to see your progress over time!")
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
    st.subheader("Accuracy Over Time")
    accuracy = df.groupby("date")["correct"].mean()
    st.line_chart(accuracy)

    # Topic Mastery
    st.subheader("Topic Mastery")
    topic_accuracy = df.groupby("topic")["correct"].mean()
    st.bar_chart(topic_accuracy)

    # Daily Study Activity
    st.subheader("Daily Study Activity")
    activity = df.groupby("date").size()
    st.bar_chart(activity)

    # Overall Mastery
    st.subheader("Overall Knowledge Mastery")
    mastery = df["correct"].mean() * 100
    st.metric("Mastery Score", f"{mastery:.2f}%")