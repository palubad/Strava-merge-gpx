import gpxpy
import gpxpy.gpx

def merge_gpx_files(files):
    """
    Merge multiple GPX files into one, sorted by timestamp.
    
    :param files: List of uploaded file-like objects
    :return: Merged GPX data as a string
    """
    merged_gpx = gpxpy.gpx.GPX()

    all_points = []  # List to store all points from all files

    for file in files:
        gpx = gpxpy.parse(file)
        
        # Collect points from all tracks in the file
        for track in gpx.tracks:
            for segment in track.segments:
                all_points.extend(segment.points)
        
        # Collect points from all routes
        for route in gpx.routes:
            all_points.extend(route.points)

        # Collect waypoints
        merged_gpx.waypoints.extend(gpx.waypoints)

    # Sort all points by time
    all_points.sort(key=lambda point: point.time)

    # Rebuild a new track with sorted points
    if all_points:
        new_track = gpxpy.gpx.GPXTrack()
        new_segment = gpxpy.gpx.GPXTrackSegment()
        new_segment.points.extend(all_points)
        new_track.segments.append(new_segment)
        merged_gpx.tracks.append(new_track)

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
