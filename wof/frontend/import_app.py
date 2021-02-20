import requests
import streamlit as st
import config

st.title("Data Importer")
# define format selector
export_format = st.selectbox("Export format", options=["Polar", "Intensity"])
# define uploader
if export_format == "Intensity":
    uploader_text = "Select your Intensity export csv file"
    uploader_kwargs = {"type": ["csv", "txt"]}
elif export_format == "Polar":
    uploader_text = "Select your Polar export json files"
    uploader_kwargs = {"type": ["json"], "accept_multiple_files": True}
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
        else:
            st.write(f"Export format '{export_format}' not supported")
    else:
        st.write("No data to upload, please select your data")
