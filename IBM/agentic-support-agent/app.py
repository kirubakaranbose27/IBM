"""
Flask web UI for the Intelligent Customer Support Agent.

Run with:
    export ANTHROPIC_API_KEY=sk-ant-...
    python app.py

Then open http://localhost:5000
"""

import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session

load_dotenv()

from agent import SupportAgent
from agent.state import ConversationState

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

agent = SupportAgent()
_conversations = {}  # conversation_id -> ConversationState (in-memory demo store)


def _get_conversation(conv_id: str) -> ConversationState:
    if conv_id not in _conversations:
        _conversations[conv_id] = ConversationState(conversation_id=conv_id)
    return _conversations[conv_id]


@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = f"user-{uuid.uuid4().hex[:8]}"
    if "conversation_id" not in session:
        session["conversation_id"] = uuid.uuid4().hex
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    user_id = session.get("user_id", "anonymous")
    conv_id = session.get("conversation_id", "default")
    conversation = _get_conversation(conv_id)

    try:
        result = agent.handle_message(user_id, conversation, user_message)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify(result)


@app.route("/api/reset", methods=["POST"])
def reset():
    conv_id = session.get("conversation_id")
    if conv_id in _conversations:
        del _conversations[conv_id]
    session["conversation_id"] = uuid.uuid4().hex
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
