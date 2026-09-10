import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import importlib.util


def _load_module(name, relpath):
    """Load a submodule directly by file path, bypassing agent/__init__.py
    (which imports the `anthropic` SDK) so these tests can run without it."""
    path = os.path.join(os.path.dirname(__file__), "..", relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Memory = _load_module("agent_memory", "agent/memory.py").Memory
ConversationState = _load_module("agent_state", "agent/state.py").ConversationState


def test_memory_persists_preferences(tmp_path):
    path = str(tmp_path / "memory.json")
    mem = Memory(path)
    mem.set_preference("user-1", "hotel_budget", "budget")

    reloaded = Memory(path)
    assert reloaded.get("user-1")["hotel_budget"] == "budget"


def test_conversation_state_tracks_tool_calls():
    state = ConversationState(conversation_id="c1")
    state.remember_tool_result("order_lookup", {"status": "Shipped"})
    assert state.tool_calls_made == 1
    assert state.scratch["order_lookup"]["status"] == "Shipped"
