"""
Weather tool.

For this prototype we return simulated data so the project runs with zero
external API keys beyond the LLM. Swap `_fake_weather` for a real weather
API call (e.g. OpenWeatherMap) in production — the tool spec and call
signature would stay the same.
"""

import random

WEATHER_SPEC = {
    "name": "get_weather",
    "description": "Get the current weather for a named city. Use this whenever the customer asks about weather.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name, e.g. 'Chennai'.",
            }
        },
        "required": ["city"],
    },
}

_CONDITIONS = ["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Thunderstorms", "Clear skies"]


def _fake_weather(city: str) -> dict:
    random.seed(city.lower())  # deterministic per city for demo reproducibility
    return {
        "city": city,
        "temperature_c": round(random.uniform(24, 36), 1),
        "condition": random.choice(_CONDITIONS),
        "humidity_pct": random.randint(40, 90),
    }


def get_weather(city: str) -> dict:
    return _fake_weather(city)
