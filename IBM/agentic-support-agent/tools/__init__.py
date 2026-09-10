"""
Tool implementations available to the agent.

Each tool is a plain Python function plus a JSON-schema style spec
compatible with the Anthropic Messages API 'tools' parameter.
"""

from .order_lookup import ORDER_LOOKUP_SPEC, order_lookup
from .calculator import CALCULATOR_SPEC, calculator
from .weather import WEATHER_SPEC, get_weather

# Registry: tool name -> (spec, callable)
TOOL_REGISTRY = {
    "order_lookup": (ORDER_LOOKUP_SPEC, order_lookup),
    "calculator": (CALCULATOR_SPEC, calculator),
    "get_weather": (WEATHER_SPEC, get_weather),
}


def all_tool_specs():
    """Return the list of tool specs to hand to the LLM."""
    return [spec for spec, _ in TOOL_REGISTRY.values()]


def run_tool(name: str, tool_input: dict):
    """Execute a registered tool by name and return its JSON-serializable result."""
    if name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool '{name}'"}
    _, fn = TOOL_REGISTRY[name]
    try:
        return fn(**tool_input)
    except Exception as exc:  # keep the agent loop alive on bad tool input
        return {"error": f"Tool '{name}' failed: {exc}"}
