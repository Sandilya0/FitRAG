def build_system_prompt() -> str:
    """System prompt for FitRAG assistant."""
    return """You are FitRAG, an expert fitness and recovery science assistant.
You answer questions about fitness recovery, sleep, HRV, nutrition, and performance
using only the provided research context.

Guidelines:
- Always base your answers on the provided research context
- Cite the source paper when referencing specific findings
- Be specific and actionable — give real numbers and timeframes when available
- If the context doesn't contain enough information, say so honestly
- Never give generic advice — always tie it back to the user's specific situation
- Keep answers clear and conversational, not overly academic
- Always end with 1-2 practical recommendations the user can act on today"""


def build_user_prompt(question: str, user_profile: dict, context_chunks: list[dict]) -> str:
    """
    Build the full prompt combining user profile + retrieved research + question.
    """

    # Format user profile
    profile_text = format_user_profile(user_profile)

    # Format research context
    context_text = format_context(context_chunks)

    prompt = f"""## User Profile
{profile_text}

## Relevant Research
{context_text}

## Question
{question}

Please answer based on the user's specific situation and the research provided.
Include citations to the source papers where relevant."""

    return prompt


def format_user_profile(profile: dict) -> str:
    """Convert user profile dict to readable text."""
    if not profile:
        return "No personal data provided."

    lines = []

    if profile.get("sleep_duration"):
        lines.append(f"- Sleep duration: {profile['sleep_duration']} hours")

    if profile.get("sleep_quality"):
        lines.append(f"- Sleep quality: {profile['sleep_quality']}")

    if profile.get("alcohol"):
        lines.append(f"- Alcohol consumed yesterday: {'Yes' if profile['alcohol'] else 'No'}")

    if profile.get("stress"):
        lines.append(f"- Stress level: {profile['stress']}")

    if profile.get("exercise_intensity"):
        lines.append(f"- Exercise intensity yesterday: {profile['exercise_intensity']}")

    if profile.get("feeling"):
        lines.append(f"- How they feel today: {profile['feeling']}")

    if profile.get("recovery_score"):
        lines.append(f"- WHOOP recovery score: {profile['recovery_score']}%")

    if profile.get("hrv"):
        lines.append(f"- HRV: {profile['hrv']}ms")

    if profile.get("resting_hr"):
        lines.append(f"- Resting heart rate: {profile['resting_hr']} bpm")

    if profile.get("notes"):
        lines.append(f"- Additional notes: {profile['notes']}")

    return "\n".join(lines) if lines else "No personal data provided."


def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into readable research context."""
    if not chunks:
        return "No relevant research found."

    context_parts = []

    for i, chunk in enumerate(chunks):
        source = chunk.get("source", "Unknown source")
        # Clean up filename for display
        source_clean = source.replace(".pdf", "").replace("_", " ")
        text = chunk.get("text", "")

        context_parts.append(f"[{i+1}] From '{source_clean}':\n{text}")

    return "\n\n".join(context_parts)