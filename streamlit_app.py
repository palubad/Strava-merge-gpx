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
