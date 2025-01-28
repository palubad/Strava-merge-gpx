import streamlit as st
import gpxpy
import gpxpy.gpx
import io

def merge_gpx_files(files):
    """
    Merge multiple GPX files into one, sorted by timestamp.

    :param files: List of uploaded file-like objects
    :return: Merged GPX data as a string
    """
    merged_gpx = gpxpy.gpx.GPX()
    all_points = []  # To store all points from all files

    for file in files:
        gpx = gpxpy.parse(file)

        # Collect points from all tracks
        for track in gpx.tracks:
            for segment in track.segments:
                all_points.extend(segment.points)

        # Collect points from all routes
        for route in gpx.routes:
            all_points.extend(route.points)

        # Collect waypoints
        merged_gpx.waypoints.extend(gpx.waypoints)

    # Sort all points by time (if time is available)
    all_points = [point for point in all_points if point.time is not None]
    all_points.sort(key=lambda point: point.time)

    # Rebuild a new track with sorted points
    if all_points:
        new_track = gpxpy.gpx.GPXTrack()
        new_segment = gpxpy.gpx.GPXTrackSegment()
        new_segment.points.extend(all_points)
        new_track.segments.append(new_segment)
        merged_gpx.tracks.append(new_track)

    return merged_gpx.to_xml()

# Streamlit app interface
st.title("GPX File Merger")
st.write("Upload multiple GPX files, and this tool will merge them into one sorted by time. You can then download the merged file.")

# File uploader
uploaded_files = st.file_uploader(
    "Upload GPX files", 
    type=["gpx"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Show list of uploaded files
    st.write("Uploaded files:")
    for uploaded_file in uploaded_files:
        st.write(f"- {uploaded_file.name}")

    # Button to trigger merging
    if st.button("Merge Files"):
        with st.spinner("Merging files..."):
            try:
                # Merge GPX files
                merged_gpx_data = merge_gpx_files(uploaded_files)

                # Convert merged data to a downloadable file
                merged_file = io.BytesIO()
                merged_file.write(merged_gpx_data.encode('utf-8'))
                merged_file.seek(0)

                # Provide a download button
                st.success("Files merged successfully!")
                st.download_button(
                    label="Download Merged GPX File",
                    data=merged_file,
                    file_name="merged_output.gpx",
                    mime="application/gpx+xml"
                )
            except Exception as e:
                st.error(f"An error occurred while merging files: {e}")
