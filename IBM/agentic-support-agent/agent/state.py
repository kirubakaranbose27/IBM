"""
Per-conversation state.

Distinct from Memory: state carries information from one workflow step
to the next *within* a single task (e.g. an order's items get passed
from the order_lookup step to a calculator step), and is discarded
once the conversation ends.
"""

from dataclasses import dataclass, field


@dataclass
class ConversationState:
    conversation_id: str
    messages: list = field(default_factory=list)      # full LLM message history
    scratch: dict = field(default_factory=dict)        # data passed between steps, e.g. last tool result
    tool_calls_made: int = 0

    def remember_tool_result(self, tool_name: str, result: dict):
        self.scratch[tool_name] = result
        self.tool_calls_made += 1
