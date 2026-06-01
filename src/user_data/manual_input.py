def build_profile_from_manual_input(answers: dict) -> dict:
    """
    Convert manual form answers into a structured user profile.
    Same format as WHOOP CSV parser output so both feed into
    the same RAG pipeline.
    """

    profile = {}

    # Sleep duration
    sleep_map = {
        "Less than 6hrs": 5.5,
        "6-7hrs": 6.5,
        "7-8hrs": 7.5,
        "8hrs+": 8.5
    }
    profile["sleep_duration"] = sleep_map.get(answers.get("sleep_duration"), None)

    # Sleep quality
    profile["sleep_quality"] = answers.get("sleep_quality", "unknown").lower()

    # Alcohol
    profile["alcohol"] = answers.get("alcohol") == "Yes"

    # Stress
    profile["stress"] = answers.get("stress", "unknown").lower()

    # Exercise
    exercise = answers.get("exercise", "No")
    if exercise == "No":
        profile["exercise_intensity"] = "none"
    else:
        profile["exercise_intensity"] = answers.get("exercise_intensity", "moderate").lower()

    # Feeling
    profile["feeling"] = answers.get("feeling", "unknown").lower()

    # Additional factors
    additional = answers.get("additional_factors", [])
    profile["late_eating"] = "Late night eating" in additional
    profile["caffeine_late"] = "Caffeine after 3pm" in additional
    profile["screen_time"] = "Lots of screen time" in additional
    profile["sick"] = "Illness/sickness" in additional

    # Notes — auto generated summary
    notes = []
    if profile["alcohol"]:
        notes.append("consumed alcohol")
    if profile["late_eating"]:
        notes.append("ate late at night")
    if profile["caffeine_late"]:
        notes.append("had caffeine after 3pm")
    if profile["sick"]:
        notes.append("feeling sick")

    profile["notes"] = ", ".join(notes) if notes else None

    return profile


def validate_profile(profile: dict) -> bool:
    """Basic validation — ensure minimum required fields are present."""
    required = ["sleep_duration", "sleep_quality", "feeling"]
    return all(profile.get(field) is not None for field in required)