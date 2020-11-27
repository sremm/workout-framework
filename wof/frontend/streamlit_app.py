import requests
import streamlit as st
from wof import config

st.title("Data Importer")

export_format = st.selectbox("Export format", options=["Intensity"])
data_file = st.file_uploader("Select your data", type=["csv", "txt"])

if st.button("Upload"):
    if data_file is not None:
        if export_format == "Intensity":
            files = {"file": data_file}
            st.write("Starting upload")
            res = requests.post(
                f"http://{config.BACKEND_IP}:{config.BACKEND_PORT}/intensity_export",
                files=files,
            )
            st.write(res)
        else:
            st.write(f"Export format '{export_format}' not supported")
    else:
        st.write("No data to upload, please select your data")
