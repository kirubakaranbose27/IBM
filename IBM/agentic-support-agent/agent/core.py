"""
Core agentic loop.

Implements the workflow described in the project report:
Input -> Understand Goal -> Decide Action -> Select Tool -> Execute Tool ->
Evaluate Result -> Update State -> Generate Response.

Uses the Anthropic Messages API for reasoning and tool selection.
"""

import os

import anthropic

from tools import all_tool_specs, run_tool
from .memory import Memory
from .prompts import build_system_prompt
from .state import ConversationState

DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
MAX_AGENT_STEPS = 6  # safety cap on tool-call loops


class SupportAgent:
    def __init__(self, api_key: str = None, memory_path: str = "data/memory.json"):
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.memory = Memory(memory_path)
        self.model = DEFAULT_MODEL

    def handle_message(self, user_id: str, conversation: ConversationState, user_message: str) -> dict:
        """
        Run one full agent turn: append the user message, loop through any
        tool calls the model requests, and return the final text response
        plus a trace of what happened (useful for the UI / demo screenshots).
        """
        conversation.messages.append({"role": "user", "content": user_message})
        preferences = self.memory.all_preferences(user_id)
        system_prompt = build_system_prompt(preferences)

        trace = []

        for _ in range(MAX_AGENT_STEPS):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                tools=all_tool_specs(),
                messages=conversation.messages,
            )

            conversation.messages.append({"role": "assistant", "content": response.content})

            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            if response.stop_reason != "tool_use" or not tool_use_blocks:
                final_text = "".join(b.text for b in response.content if b.type == "text")
                self._maybe_store_preference(user_id, user_message)
                return {"reply": final_text, "trace": trace}

            tool_results = []
            for block in tool_use_blocks:
                result = run_tool(block.name, block.input)
                conversation.remember_tool_result(block.name, result)
                trace.append({"tool": block.name, "input": block.input, "result": result})
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    }
                )

            conversation.messages.append({"role": "user", "content": tool_results})

        return {
            "reply": "I'm sorry, I wasn't able to complete that request. Could you rephrase it?",
            "trace": trace,
        }

    def _maybe_store_preference(self, user_id: str, user_message: str):
        """Very small heuristic memory writer, matching the report's example
        of remembering a preference like 'budget hotels'. In a production
        system this would be a dedicated extraction step."""
        lowered = user_message.lower()
        if "prefer" in lowered or "i like" in lowered:
            self.memory.set_preference(user_id, "note", user_message)
