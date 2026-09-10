# Intelligent Customer Support Agent (Agentic AI)

A working implementation of an agentic customer-support system, built for the
IBM / Naan Mudhalvan Agentic AI internship project. The agent understands a
customer request, decides whether it needs a tool, calls the tool, evaluates
the result, and produces a final response — following the classic agent loop:

```
Input → Understand Goal → Decide Action → Select Tool → Execute Tool →
Evaluate Result → Update State → Generate Response
```

## Features

- **Tool integration** — order lookup, calculator, and weather tools the agent can call.
- **Memory** — lightweight persisted user preferences (e.g. "I prefer budget hotels").
- **State** — per-conversation scratch data passed between workflow steps (e.g. an order's items flow from `order_lookup` into `calculator`).
- **Multi-step tool use** — the agent can chain tool calls (e.g. look up an order, then compute its total) before answering.
- **Web UI** — a small Flask chat console that also shows a live trace of every tool call the agent makes, for demo/screenshot purposes.

## Architecture

```
.
├── app.py                 # Flask web server + chat/reset API
├── agent/
│   ├── core.py             # The agent loop (calls the Anthropic API, runs tools)
│   ├── memory.py           # Persisted long-term preferences (JSON-backed)
│   ├── state.py            # Per-conversation state/scratch data
│   └── prompts.py          # System prompt construction
├── tools/
│   ├── order_lookup.py     # Simulated order database tool
│   ├── calculator.py       # Safe arithmetic evaluator tool
│   └── weather.py          # Simulated weather tool
├── data/
│   └── orders.json         # Sample order data used by order_lookup
├── templates/index.html    # Chat UI markup
├── static/                 # Chat UI styling + JS
└── tests/                  # Unit tests for tools, memory, and state
```

## Setup

**Requirements:** Python 3.10+, an [Anthropic API key](https://console.anthropic.com/).

```bash
git clone https://github.com/<your-username>/agentic-support-agent.git
cd agentic-support-agent

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# then edit .env and add your ANTHROPIC_API_KEY
```

## Run

```bash
python app.py
```

Open **http://localhost:5000** and try:

- "Check order 1025 and tell me the total"
- "What's the status of order 1042?"
- "What's the weather in Chennai?"
- "I prefer budget options" (stored as a remembered preference)

Sample order IDs available in `data/orders.json`: `1025`, `1042`, `1088`.

## Running tests

Tests for the tools, memory, and state modules run without an API key:

```bash
pip install pytest
pytest tests/ -v
```

## How each report section maps to code

| Report section | Where it lives |
|---|---|
| Workflow (Input → Decide → Tool → Evaluate → Response) | `agent/core.py: SupportAgent.handle_message` |
| Tool integration | `tools/` package + `TOOL_REGISTRY` in `tools/__init__.py` |
| Memory | `agent/memory.py` |
| State | `agent/state.py` |
| Multi-step workflow / demonstrations | Flask UI trace panel (`static/chat.js`, `templates/index.html`) |

## Extending it

- **Add a tool:** create `tools/your_tool.py` exporting a `_SPEC` dict and a function, then register it in `tools/__init__.py`'s `TOOL_REGISTRY`.
- **Connect a real database:** swap `tools/order_lookup.py`'s JSON file read for a real DB/API call — the tool spec and calling convention stay the same.
- **Real weather data:** replace `tools/weather.py`'s simulated response with a call to a weather API (e.g. OpenWeatherMap), gated behind its own API key.

## Future enhancements (from the project report)

- Authentication and role-based access
- Real customer/order database connection
- Additional tools: payment, shipment tracking, ticket creation
- Monitoring and error handling
- Multilingual support
- Improved memory controls and privacy
- Larger-scale evaluation

## License

MIT — see [LICENSE](LICENSE).
