"""
Order lookup tool.

Simulates a structured order database. In production this would call
a real order-management API or database instead of reading a JSON file.
"""

import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "orders.json")

ORDER_LOOKUP_SPEC = {
    "name": "order_lookup",
    "description": (
        "Look up a customer order by its order ID. Returns the order status, "
        "estimated delivery date, and the list of items with prices and quantities. "
        "Use this whenever the customer asks about an order's status, contents, or delivery."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID to look up, e.g. '1025'.",
            }
        },
        "required": ["order_id"],
    },
}


def _load_orders():
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def order_lookup(order_id: str) -> dict:
    orders = _load_orders()
    order = orders.get(str(order_id))
    if not order:
        return {"found": False, "order_id": order_id, "message": "No order found with this ID."}

    subtotal = sum(item["price"] * item["qty"] for item in order["items"])
    return {
        "found": True,
        "order_id": order_id,
        "customer": order["customer"],
        "status": order["status"],
        "eta": order["eta"],
        "items": order["items"],
        "subtotal": round(subtotal, 2),
    }
