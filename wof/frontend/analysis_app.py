from typing import Dict

import requests
import streamlit as st

st.set_page_config(layout="wide")
st.title("Workout Analysis")

# Date selector
col1, col2 = st.beta_columns(2)
start_date = col1.date_input("Start date")
end_date = col2.date_input("End date")


@st.cache
def get_summary(start_date, end_date) -> Dict:
    print("fetcing data")
    # response = requests.get("analytics/workout_sessions_summary")
    # parser response
    result = {"start": str(start_date), "end": str(end_date)}
    return result


summary = get_summary(start_date, end_date)
st.write(summary)
