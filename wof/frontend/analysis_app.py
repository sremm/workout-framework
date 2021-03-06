from datetime import date, datetime
from typing import Dict

import config

# import ptvsd
import requests
import streamlit as st

# ptvsd.enable_attach(address=("localhost", 5678))
# # ptvsd.wait_for_attach()  # Only include this line if you always wan't to attach the debugger


def convert_to_datetime(date: date) -> datetime:
    return datetime(date.year, date.month, date.day)


st.set_page_config(layout="wide")
st.title("Workout Analysis")

# Date selector
col1, col2 = st.beta_columns(2)
start_date = convert_to_datetime(col1.date_input("Start date"))
end_date = convert_to_datetime(col2.date_input("End date"))


@st.cache
def get_summary(start_date, end_date) -> Dict:
    print(start_date)
    print(end_date)
    print("fetcing data")
    res = requests.get(
        f"{config.get_api_url()}/analytics/workout_session_summary",
        params=(("start", str(start_date)), ("end", end_date)),
    )
    return res.json()


summary = {}
if st.button("Fetch"):
    summary = get_summary(start_date, end_date)
st.write(summary)
