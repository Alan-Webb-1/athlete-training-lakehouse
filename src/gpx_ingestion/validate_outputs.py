from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACTIVITIES_CLEAN = PROJECT_ROOT / "data" / "processed" / "activities" / "activities_clean.csv"
TRACKPOINTS = PROJECT_ROOT / "data" / "processed" / "trackpoints" / "trackpoints.csv"
LOG_FILE = PROJECT_ROOT / "data" / "processed" / "logs" / "validation_log.csv"


def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_activities(activities):
    validation_results = []

    for row in activities:
        activity_id = row["activity_id"]

        checks = [
            {
                "activity_id": activity_id,
                "check_name": "distance_miles_positive",
                "passed": float(row["distance_miles"]) > 0,
                "value_checked": row["distance_miles"]
            },
            {
                "activity_id": activity_id,
                "check_name": "duration_minutes_positive",
                "passed": float(row["duration_minutes"]) > 0,
                "value_checked": row["duration_minutes"]
            },
            {
                "activity_id": activity_id,
                "check_name": "trackpoint_count_positive",
                "passed": int(row["trackpoint_count"]) > 0,
                "value_checked": row["trackpoint_count"]
            },
            {
                "activity_id": activity_id,
                "check_name": "reasonable_running_distance",
                "passed": 0 < float(row["distance_miles"]) < 30,
                "value_checked": row["distance_miles"]
            },
            {
                "activity_id": activity_id,
                "check_name": "reasonable_duration",
                "passed": 0 < float(row["duration_minutes"]) < 300,
                "value_checked": row["duration_minutes"]
            }
        ]

        validation_results.extend(checks)

    return validation_results


def main():
    activities = read_csv(ACTIVITIES_CLEAN)

    validation_results = validate_activities(activities)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "activity_id",
            "check_name",
            "passed",
            "value_checked"
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(validation_results)

    total_checks = len(validation_results)
    passed_checks = sum(1 for result in validation_results if result["passed"] is True)
    failed_checks = total_checks - passed_checks

    print("Validation complete.")
    print(f"Activities validated: {len(activities)}")
    print(f"Total checks: {total_checks}")
    print(f"Passed checks: {passed_checks}")
    print(f"Failed checks: {failed_checks}")
    print(f"Validation log written to: {LOG_FILE}")


if __name__ == "__main__":
    main()