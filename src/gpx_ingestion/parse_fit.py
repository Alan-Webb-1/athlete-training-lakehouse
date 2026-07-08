from pathlib import Path
import gzip
import csv
from fitparse import FitFile


RAW_FIT_DIR = Path(r"C:\GPX_Processing\raw_fit_gz")
OUTPUT_DIR = Path(r"C:\GPX_Processing\processed")
OUTPUT_FILE = OUTPUT_DIR / "fit_activity_summary.csv"


def parse_fit_gz(file_path: Path, athlete_name: str) -> dict | None:
    try:
        with gzip.open(file_path, "rb") as f:
            fitfile = FitFile(f)

            activity_start_time = None
            total_distance_meters = None
            total_timer_time_seconds = None
            total_ascent_feet = None

            for record in fitfile.get_messages("session"):
                for field in record:
                    if field.name == "start_time":
                        activity_start_time = field.value
                    elif field.name == "total_distance":
                        total_distance_meters = field.value
                    elif field.name == "total_timer_time":
                        total_timer_time_seconds = field.value
                    elif field.name == "total_ascent":
                        total_ascent_feet = field.value * 3.28084 if field.value is not None else None

            if activity_start_time is None or total_distance_meters is None:
                return None

            distance_miles = total_distance_meters / 1609.344
            duration_minutes = total_timer_time_seconds / 60 if total_timer_time_seconds else None

            return {
                "athlete_name": athlete_name,
                "source_file": file_path.name,
                "source_format": "fit.gz",
                "activity_start_time": activity_start_time,
                "distance_miles": round(distance_miles, 2),
                "duration_minutes": round(duration_minutes, 2) if duration_minutes else None,
                "elevation_gain_feet": round(total_ascent_feet, 2) if total_ascent_feet else None,
            }

    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return None


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    for athlete_folder in RAW_FIT_DIR.iterdir():
        if athlete_folder.is_dir():
            athlete_name = athlete_folder.name

            for fit_file in athlete_folder.glob("*.fit.gz"):
                parsed = parse_fit_gz(fit_file, athlete_name)
                if parsed:
                    rows.append(parsed)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "athlete_name",
                "source_file",
                "source_format",
                "activity_start_time",
                "distance_miles",
                "duration_minutes",
                "elevation_gain_feet",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsed FIT activities: {len(rows)}")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()