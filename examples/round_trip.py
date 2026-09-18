"""Run after installing the project: python examples/round_trip.py."""

import json
from hairbridge import human_to_ai_translate, ai_to_human_translate

bridge = human_to_ai_translate(
    "Make mine look like this.",
    context="User provides a UI screenshot with substantially different structure.",
)
print(json.dumps(bridge.to_dict(), indent=2))
print(ai_to_human_translate(bridge))
