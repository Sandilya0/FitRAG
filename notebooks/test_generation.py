import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generation.answer_generator import ask

# Test 1 — no user profile
print("=" * 60)
result = ask("Does creatine help with muscle recovery?")
print("\nANSWER:")
print(result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print(f"  - {s}")

# Test 2 — with user profile
print("\n" + "=" * 60)
user_profile = {
    "sleep_duration": 8.5,
    "sleep_quality": "poor",
    "alcohol": True,
    "stress": "high",
    "exercise_intensity": "heavy",
    "feeling": "tired"
}

result2 = ask(
    "I slept 8.5 hours but feel terrible, why is my recovery low?",
    user_profile=user_profile
)
print("\nANSWER:")
print(result2["answer"])
print("\nSOURCES:")
for s in result2["sources"]:
    print(f"  - {s}")

    # Test manual input
print("\n" + "=" * 60)
print("Testing manual input parser...")
from src.user_data.manual_input import build_profile_from_manual_input

answers = {
    "sleep_duration": "8hrs+",
    "sleep_quality": "Poor",
    "alcohol": "Yes",
    "stress": "High",
    "exercise": "Yes",
    "exercise_intensity": "Heavy",
    "feeling": "Tired",
    "additional_factors": ["Late night eating", "Caffeine after 3pm"]
}

profile = build_profile_from_manual_input(answers)
print("Profile built:", profile)

# Test with RAG
result3 = ask(
    "Why do I feel so tired today?",
    user_profile=profile
)
print("\nANSWER:")
print(result3["answer"])