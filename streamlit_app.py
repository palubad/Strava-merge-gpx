import streamlit as st
import gpxpy
import gpxpy.gpx
import io

def merge_gpx_files(files):
    """
    Merge multiple GPX files into one.
    
    :param files: List of uploaded file-like objects
    :return: Merged GPX data as a string
    """
    merged_gpx = gpxpy.gpx.GPX()

    for file in files:
        gpx = gpxpy.parse(file)
        merged_gpx.tracks.extend(gpx.tracks)
        merged_gpx.routes.extend(gpx.routes)
        merged_gpx.waypoints.extend(gpx.waypoints)

    return merged_gpx.to_xml()

# Streamlit app
st.title("GPX File Merger")
st.write("Upload multiple GPX files to merge them into a single file.")

# File uploader
uploaded_files = st.file_uploader(
    "Upload GPX files", 
    type=["gpx"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Button to trigger the merge process
    if st.button("Merge Files"):
        with st.spinner("Merging files..."):
            # Merge GPX files
            merged_gpx_data = merge_gpx_files(uploaded_files)

            # Convert merged data to a downloadable file
            merged_file = io.BytesIO()
            merged_file.write(merged_gpx_data.encode('utf-8'))
            merged_file.seek(0)

            # Provide a download link
            st.success("Files merged successfully!")
            st.download_button(
                label="Download Merged GPX File",
                data=merged_file,
                file_name="merged_output.gpx",
                mime="application/gpx+xml"
            )
