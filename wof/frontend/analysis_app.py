from datetime import date, datetime
from typing import Dict, Optional

import config

# import ptvsd
import requests
import streamlit as st
from wof.domain import analytics, model

# ptvsd.enable_attach(address=("localhost", 5678))
# # ptvsd.wait_for_attach()  # Only include this line if you always wan't to attach the debugger


def convert_to_datetime(date: date) -> datetime:
    return datetime(date.year, date.month, date.day)


st.set_page_config(layout="wide")
st.title("Workout Analysis")

# Date selector
st.header("Summary for period")
col1, col2 = st.beta_columns(2)
start_date = convert_to_datetime(col1.date_input("Start date"))
end_date = convert_to_datetime(col2.date_input("End date"))


@st.cache
def get_summary_data(start_date, end_date) -> analytics.WorkoutSessionsSummary:
    print(start_date)
    print(end_date)
    print("fetcing data")
    res = requests.get(
        f"{config.get_api_url()}/analytics/workout_session_summary",
        params=(("start", str(start_date)), ("end", end_date)),
    )
    return analytics.WorkoutSessionsSummary(**res.json())


def summary_view(data: analytics.WorkoutSessionsSummary):
    col1, col2 = st.beta_columns([1, 1])
    # set stats

    col1.markdown(
        f"""
    ## Totals:
    - Reps: {data.workout_set_stats.total_reps}
    - Weight: {data.workout_set_stats.total_weight} {data.workout_set_stats.weight_unit}
    - Average per rep: {data.workout_set_stats.total_weight/data.workout_set_stats.total_reps:.1f} kg/rep
    """
    )

    # hr stats
    col2.markdown(
        f"""
    ## Heart rate stats:
    Calculated as mean over all sessions, eg. mean of max values etc.
    - Mean: {data.heart_rate_stats.mean:.0f} bpm
    - Std: {data.heart_rate_stats.std:.0f} bpm
    - Max: {data.heart_rate_stats.max:.0f} bpm
    - Min: {data.heart_rate_stats.min:.0f} bpm
    """
    )


summary_data = get_summary_data(start_date, end_date)
summary_view(summary_data)
st.header("Last Session")


def get_last_session(session_type_name: Optional[str] = None) -> model.WorkoutSession:
    # res = request.get("/workout_session/last_session",params=(("type","Strength Training")))
    return model.WorkoutSession(type=model.SessionType(name=session_type_name))


last_strength_session = get_last_session(session_type_name="Strength training")


def session_view(data: model.WorkoutSession):
    st.write("Session type: ", data.type.name)

    # do some nice table to get an overview of excercises
    # Excercise - Squats        - Deadlift
    #             10 reps 10 kg   8 reps 20 kg
    #             10 reps 10 kg   8 reps 20 kg

    # gather sets per excercise
    # create a column for each exercise
    for cur_set in data.sets:
        st.write(cur_set)

    # plot hr
    if data.heart_rate is not None:
        st.line_chart(last_strength_session)


session_view(last_strength_session)
