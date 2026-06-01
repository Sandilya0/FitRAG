from groq import Groq
from src.utils.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS


def get_groq_client():
    """Initialize Groq client."""
    return Groq(api_key=GROQ_API_KEY)


def generate_response(system_prompt: str, user_prompt: str) -> str:
    """
    Send prompt to Groq and return the response.
    """
    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=GROQ_TEMPERATURE,
        max_tokens=GROQ_MAX_TOKENS
    )

    return response.choices[0].message.content