from pathlib import Path
import pandas as pd

from wof.import_logic import intensity_app

import streamlit as st

data_path = list(Path("data", "Intensity").glob("*.csv"))[0]

all_sessions = intensity_app.import_from_file(data_path)

st.write(f"Total sessions: {len(all_sessions)}")
