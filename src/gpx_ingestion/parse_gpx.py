from pathlib import Path
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2


# -----------------------------
# Helper function: calculate distance between GPS points
# -----------------------------

def haversine_miles(lat1, lon1, lat2, lon2):
    """
    Calculate distance in miles between two latitude/longitude points.
    """
    earth_radius_miles = 3958.8

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_miles * c


# -----------------------------
# File paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_GPX_DIR = PROJECT_ROOT / "data" / "raw_gpx" / "alan"
ACTIVITIES_OUTPUT = PROJECT_ROOT / "data" / "processed" / "activities" / "activities.csv"
CLEAN_ACTIVITIES_OUTPUT = PROJECT_ROOT / "data" / "processed" / "activities" / "activities_clean.csv"
TRACKPOINTS_OUTPUT = PROJECT_ROOT / "data" / "processed" / "trackpoints" / "trackpoints.csv"
LOG_OUTPUT = PROJECT_ROOT / "data" / "processed" / "logs" / "pipeline_run_log.csv"


# -----------------------------
# Main parser
# -----------------------------

def parse_gpx_file(file_path, activity_id, athlete_id=1, athlete_name="Alan Webb"):
    """
    Parse one GPX file and return:
    1. One activity row
    2. Many trackpoint rows
    3. One log row
    """

    trackpoints = []

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

        trkpts = root.findall(".//gpx:trkpt", namespace)

        total_distance_miles = 0
        total_elevation_gain_meters = 0

        previous_lat = None
        previous_lon = None
        previous_ele = None

        start_time = None
        end_time = None

        for i, trkpt in enumerate(trkpts, start=1):
            lat = float(trkpt.attrib["lat"])
            lon = float(trkpt.attrib["lon"])

            ele_element = trkpt.find("gpx:ele", namespace)
            time_element = trkpt.find("gpx:time", namespace)

            elevation_meters = float(ele_element.text) if ele_element is not None else None
            timestamp = time_element.text if time_element is not None else None

            if timestamp:
                timestamp_clean = timestamp.replace("Z", "+00:00")
                current_time = datetime.fromisoformat(timestamp_clean)

                if start_time is None:
                    start_time = current_time

                end_time = current_time

            if previous_lat is not None and previous_lon is not None:
                total_distance_miles += haversine_miles(
                    previous_lat,
                    previous_lon,
                    lat,
                    lon
                )

            if previous_ele is not None and elevation_meters is not None:
                elevation_change = elevation_meters - previous_ele
                if elevation_change > 0:
                    total_elevation_gain_meters += elevation_change

            trackpoints.append({
                "activity_id": activity_id,
                "trackpoint_number": i,
                "timestamp": timestamp,
                "latitude": lat,
                "longitude": lon,
                "elevation_meters": elevation_meters
            })

            previous_lat = lat
            previous_lon = lon
            previous_ele = elevation_meters

        duration_minutes = None
        if start_time and end_time:
            duration_minutes = (end_time - start_time).total_seconds() / 60

        elevation_gain_feet = total_elevation_gain_meters * 3.28084

        activity = {
            "activity_id": activity_id,
            "athlete_id": athlete_id,
            "athlete_name": athlete_name,
            "source_file": file_path.name,
            "activity_start_time": start_time,
            "activity_end_time": end_time,
            "duration_minutes": round(duration_minutes, 2) if duration_minutes else None,
            "distance_miles": round(total_distance_miles, 2),
            "elevation_gain_feet": round(elevation_gain_feet, 2),
            "trackpoint_count": len(trackpoints),
            "loaded_at": datetime.now()
        }

        log = {
            "activity_id": activity_id,
            "source_file": file_path.name,
            "status": "success",
            "records_parsed": len(trackpoints),
            "error_message": "",
            "loaded_at": datetime.now()
        }

        return activity, trackpoints, log

    except Exception as e:
        activity = None
        trackpoints = []

        log = {
            "activity_id": activity_id,
            "source_file": file_path.name,
            "status": "failed",
            "records_parsed": 0,
            "error_message": str(e),
            "loaded_at": datetime.now()
        }

        return activity, trackpoints, log


# -----------------------------
# Run parser for all GPX files
# -----------------------------

def main():
    activities = []
    all_trackpoints = []
    logs = []

    gpx_files = sorted(RAW_GPX_DIR.glob("*.gpx"))

    seen_activities = {}

    for activity_id, file_path in enumerate(gpx_files, start=1):
        activity, trackpoints, log = parse_gpx_file(file_path, activity_id)

        if activity:
            duplicate_key = (
                activity["athlete_id"],
                activity["activity_start_time"],
                activity["duration_minutes"],
                activity["distance_miles"]
            )

            if duplicate_key in seen_activities:
                activity["duplicate_activity_flag"] = True
                activity["duplicate_of_activity_id"] = seen_activities[duplicate_key]
                log["status"] = "duplicate"
                log["error_message"] = f"Duplicate of activity_id {seen_activities[duplicate_key]}"
            else:
                activity["duplicate_activity_flag"] = False
                activity["duplicate_of_activity_id"] = ""
                seen_activities[duplicate_key] = activity["activity_id"]

            activities.append(activity)

        all_trackpoints.extend(trackpoints)
        logs.append(log)

    ACTIVITIES_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    TRACKPOINTS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    clean_activities = [
        activity for activity in activities
        if activity["duplicate_activity_flag"] == False
    ]

    if activities:
        with open(ACTIVITIES_OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=activities[0].keys())
            writer.writeheader()
            writer.writerows(activities)

    if clean_activities:
        with open(CLEAN_ACTIVITIES_OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=clean_activities[0].keys())
            writer.writeheader()
            writer.writerows(clean_activities)

    if all_trackpoints:
        with open(TRACKPOINTS_OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_trackpoints[0].keys())
            writer.writeheader()
            writer.writerows(all_trackpoints)

    if logs:
        with open(LOG_OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=logs[0].keys())
            writer.writeheader()
            writer.writerows(logs)

    print("GPX parsing complete.")
    print(f"Activities written to: {ACTIVITIES_OUTPUT}")
    print(f"Clean activities written to: {CLEAN_ACTIVITIES_OUTPUT}")
    print(f"Trackpoints written to: {TRACKPOINTS_OUTPUT}")
    print(f"Logs written to: {LOG_OUTPUT}")
    print(f"GPX files processed: {len(gpx_files)}")


if __name__ == "__main__":
    main()