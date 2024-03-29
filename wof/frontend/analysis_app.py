import enum
from collections import defaultdict
from datetime import date, datetime
from typing import DefaultDict, Dict, List, Optional, Tuple

import config
import plotly.graph_objects as go

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
start_date = convert_to_datetime(col1.date_input("Start date", value=date(2021, 1, 1)))
end_date = convert_to_datetime(col2.date_input("End date", value=date(2021, 1, 31)))


@st.cache
def get_summary_data(start_date, end_date) -> analytics.WorkoutSessionsSummary:
    print("fetching data", start_date, end_date)
    res = requests.get(
        f"{config.get_api_url()}/analytics/workout_session_summary",
        params=(("start", start_date), ("end", end_date)),
    )
    return analytics.WorkoutSessionsSummary(**res.json())


def summary_view(data: analytics.WorkoutSessionsSummary):
    col1, col2 = st.beta_columns([1, 1])
    # set stats

    kg_per_rep = (
        data.workout_set_stats.total_weight / data.workout_set_stats.total_reps
        if data.workout_set_stats.total_reps != 0
        else 0
    )
    col1.markdown(
        f"""
        ## Totals:
        - Number of sessions: {len(data.session_ids)}
        - Reps: {data.workout_set_stats.total_reps}
        - Weight: {data.workout_set_stats.total_weight} {data.workout_set_stats.weight_unit}
        - Average per rep: {kg_per_rep:.1f} kg/rep
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
st.markdown("---")
st.header("Last session in period")


@st.cache(allow_output_mutation=True)
def get_sessions_in_range(start_date, end_date) -> List[model.WorkoutSession]:
    res = requests.get(f"{config.get_api_url()}/workout_sessions", params=(("start", start_date), ("end", end_date)))
    return [model.WorkoutSession(**x) for x in res.json()]


sessions_in_range = get_sessions_in_range(start_date, end_date)


def session_view(data: model.WorkoutSession):
    st.write("Date: ", data.start_time, "Session type: ", data.type.name)

    if data.sets != []:
        st.subheader("Exercises")
        per_exercise: DefaultDict[str, List] = defaultdict(list)
        for cur_set in data.sets:
            per_exercise[cur_set.exercise].append(cur_set)
        cols = st.beta_columns(len(per_exercise))
        for idx, (key, vals) in enumerate(per_exercise.items()):
            cols[idx].text(key)
            for cur_set in vals:
                cols[idx].write(f"{cur_set.reps} x {cur_set.weights} {cur_set.unit}")

    if data.heart_rate is not None:
        st.subheader("Heart rate")
        fig = go.Figure()
        fig.add_scatter(x=data.heart_rate.time, y=data.heart_rate.values)
        st.plotly_chart(fig)


st.markdown("---")

if sessions_in_range != []:
    selected_session_idx = st.selectbox("Select session", options=[x for x in range(len(sessions_in_range))], index=0)
    session_view(sessions_in_range[selected_session_idx])

st.markdown("---")


def strenght_training_sessions_view(sessions: List[model.WorkoutSession], desired_excercises: List[str], max_cols):
    """ filters out non strenght training sessions and shows interesting information about the desired excercises sessions """
    st.write("Strenght training sessions")
    strength_sessions = [x for x in sessions if x.type.name == "Strength training"]

    sets_per_session: List[Tuple[datetime, str, List[model.WorkoutSet]]] = []
    for sess in strength_sessions:
        if sess.sets != []:
            per_exercise: DefaultDict[str, List] = defaultdict(list)
            for cur_set in sess.sets:
                if cur_set.exercise in desired_excercises:
                    per_exercise[cur_set.exercise].append(cur_set)
            if per_exercise != {}:
                for excercise_name, sets in per_exercise.items():
                    sets_per_session.append((sess.start_time, excercise_name, sets))

    num_items = len(sets_per_session)
    num_rows = num_items // max_cols + 1
    num_cols = num_items if num_items <= max_cols else max_cols
    grid = [st.beta_columns(num_cols) for _ in range(num_rows)]
    for idx, (start_time, name, sets) in enumerate(sets_per_session):
        cur_row = abs((num_cols - (idx + 1)) // num_cols)
        cur_col = idx - num_cols * cur_row
        col = grid[cur_row][cur_col]

        col.write(f"Date: {start_time}")
        iso_cal = start_time.isocalendar()
        col.write(f"W-{iso_cal.week} D-{iso_cal.weekday}")
        col.write(name)
        for cur_set in sets:
            col.write(f"{cur_set.reps} x {cur_set.weights} {cur_set.unit}")


excersises = st.text_input("Desired excercise [multiple with commas]", value="Squats")
max_cols = st.number_input("max columns", value=12)
desired_excercises = excersises.split(",")
strenght_training_sessions_view(sessions_in_range, desired_excercises, max_cols)
