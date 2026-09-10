try:
    from .core import SupportAgent

    __all__ = ["SupportAgent"]
except ImportError:
    # Allows `agent.memory` / `agent.state` to be imported (e.g. in tests)
    # without the `anthropic` package installed. SupportAgent itself still
    # requires `pip install anthropic` to import successfully.
    __all__ = []
