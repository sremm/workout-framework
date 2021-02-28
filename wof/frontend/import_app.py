import ptvsd
import requests
import streamlit as st

import config

ptvsd.enable_attach(address=("localhost", 5678))
# ptvsd.wait_for_attach()  # Only include this line if you always wan't to attach the debugger

st.title("Data Importer")
# define format selector
export_format = st.selectbox("Export format", options=["Polar", "Intensity", "PolarAndIntensity"])
# define uploader
if export_format == "Intensity":
    uploader_text = "Select your Intensity export csv file"
    uploader_kwargs = {"type": ["csv"]}
elif export_format == "Polar":
    uploader_text = "Select your Polar export json files"
    uploader_kwargs = {"type": ["json"], "accept_multiple_files": True}
elif export_format == "PolarAndIntensity":
    uploader_text = "Select your polar and intensity data"
    uploader_kwargs = {"type": ["csv", "json"], "accept_multiple_files": True}
else:
    uploader_text = "export format not supported"
    uploader_kwargs = {"type": [""]}

uploaded = st.file_uploader(uploader_text, **uploader_kwargs)

# add button and its logic
if st.button("Upload"):
    if uploaded is not None:
        if export_format == "Intensity":
            files = {"file": uploaded}
            st.write("Starting upload")
            res = requests.post(
                f"{config.get_api_url()}/import/intensity",
                files=files,
            )
            st.write(res)
        elif export_format == "Polar":
            files = [("files", x) for x in uploaded]
            print(files)
            st.write("Starting upload")
            res = requests.post(
                f"{config.get_api_url()}/import/polar",
                files=files,
            )
            st.write(res)
        elif export_format == "PolarAndIntensity":
            # all json files as polar_files
            polar_files = [("polar_files", x) for x in uploaded if ".json" in x.name]
            # the csv file as intensity_file
            intensity_files = [("intensity_file", x) for x in uploaded if ".csv" in x.name]
            assert len(polar_files) >= 1, "No polar files .json found"
            assert len(intensity_files) == 1, "Found more than 1 or 0 intensity files"
            files = [*polar_files, *intensity_files]
            st.write("Starting upload")
            res = requests.post(
                f"{config.get_api_url()}/import/polar_and_intensity_with_merge",
                files=files,
            )
            st.write(res)
        else:
            st.write(f"Export format '{export_format}' not supported")
    else:
        st.write("No data to upload, please select your data")
