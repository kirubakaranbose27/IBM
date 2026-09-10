"""
Calculator tool.

Gives the agent a way to produce exact numeric results (e.g. order totals,
discounts, tax) instead of letting the LLM guess arithmetic from text.
"""

import ast
import operator as op

CALCULATOR_SPEC = {
    "name": "calculator",
    "description": (
        "Evaluate a basic arithmetic expression and return an exact numeric result. "
        "Use this for totals, discounts, tax, or any calculation instead of estimating."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A basic arithmetic expression, e.g. '799 + 2*299' or '(1299+399)*0.9'.",
            }
        },
        "required": ["expression"],
    },
}

# Only allow safe arithmetic operators — never eval() raw user/LLM input.
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Expression contains disallowed syntax.")


def calculator(expression: str) -> dict:
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return {"expression": expression, "result": round(result, 4) if isinstance(result, float) else result}
    except Exception as exc:
        return {"expression": expression, "error": f"Could not evaluate expression: {exc}"}
