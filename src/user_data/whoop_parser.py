import pandas as pd
import os


def parse_whoop_csv(file_path: str) -> dict:
    """
    Parse WHOOP export CSV and extract the most recent day's metrics.
    Returns a user profile dict in the same format as manual input.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"WHOOP CSV not found: {file_path}")

    df = pd.read_csv(file_path)

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Sort by date and get most recent row
    date_col = next((c for c in df.columns if "date" in c or "cycle" in c), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(date_col, ascending=False)

    latest = df.iloc[0]

    profile = {}

    # Recovery score
    recovery_col = next((c for c in df.columns if "recovery" in c), None)
    if recovery_col:
        profile["recovery_score"] = safe_float(latest.get(recovery_col))

    # HRV
    hrv_col = next((c for c in df.columns if "hrv" in c), None)
    if hrv_col:
        profile["hrv"] = safe_float(latest.get(hrv_col))

    # Resting heart rate
    rhr_col = next((c for c in df.columns if "resting" in c and "heart" in c), None)
    if rhr_col:
        profile["resting_hr"] = safe_float(latest.get(rhr_col))

    # Sleep duration
    sleep_col = next((c for c in df.columns if "sleep" in c and "duration" in c), None)
    if sleep_col:
        profile["sleep_duration"] = safe_float(latest.get(sleep_col))

    # Sleep quality / performance
    sleep_perf_col = next((c for c in df.columns if "sleep" in c and "performance" in c), None)
    if sleep_perf_col:
        score = safe_float(latest.get(sleep_perf_col))
        if score:
            if score >= 85:
                profile["sleep_quality"] = "great"
            elif score >= 70:
                profile["sleep_quality"] = "good"
            elif score >= 50:
                profile["sleep_quality"] = "average"
            else:
                profile["sleep_quality"] = "poor"

    # Strain
    strain_col = next((c for c in df.columns if "strain" in c), None)
    if strain_col:
        strain = safe_float(latest.get(strain_col))
        if strain:
            if strain >= 18:
                profile["exercise_intensity"] = "heavy"
            elif strain >= 12:
                profile["exercise_intensity"] = "moderate"
            else:
                profile["exercise_intensity"] = "light"

    # Defaults for fields not in WHOOP export
    profile.setdefault("alcohol", False)
    profile.setdefault("stress", "unknown")
    profile.setdefault("feeling", "unknown")
    profile.setdefault("notes", None)

    return profile


def safe_float(value) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_whoop_summary(profile: dict) -> str:
    """Generate a human readable summary of WHOOP metrics."""
    lines = []

    if profile.get("recovery_score"):
        lines.append(f"Recovery: {profile['recovery_score']}%")
    if profile.get("hrv"):
        lines.append(f"HRV: {profile['hrv']}ms")
    if profile.get("resting_hr"):
        lines.append(f"Resting HR: {profile['resting_hr']} bpm")
    if profile.get("sleep_duration"):
        lines.append(f"Sleep: {profile['sleep_duration']} hours")
    if profile.get("sleep_quality"):
        lines.append(f"Sleep quality: {profile['sleep_quality']}")
    if profile.get("exercise_intensity"):
        lines.append(f"Yesterday's strain: {profile['exercise_intensity']}")

    return " | ".join(lines) if lines else "No WHOOP data available"