import ast
import operator
import re
from pathlib import Path
from urllib.parse import urlparse

import requests


# -----------------------------
# Safe calculator
# -----------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculator(expression: str) -> str:
    """Safely evaluate simple arithmetic expressions."""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return str(result)

    except Exception as error:
        return (
            f"Calculator error: {error}. "
            "Use only numbers and + - * / ( )."
        )


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed")

    if isinstance(node, ast.UnaryOp):
        operator_function = ALLOWED_OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported operator")

        return operator_function(_eval_node(node.operand))

    if isinstance(node, ast.BinOp):
        operator_function = ALLOWED_OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported operator")

        left = _eval_node(node.left)
        right = _eval_node(node.right)

        return operator_function(left, right)

    raise ValueError("Only numbers and + - * / ( ) are allowed")


# -----------------------------
# Webpage reader
# -----------------------------

def read_webpage(url: str, max_chars: int = 2000) -> str:
    """
    Read a local HTML file or webpage.

    max_chars is intentionally limited to 2000 characters
    to prevent sending very large content to the model.
    """

    try:
        parsed = urlparse(url)

        # Local file
        if not parsed.scheme:
            path = Path(url)

            if not path.exists():
                return (
                    f"Read error: '{url}' is not a URL "
                    "and no such file exists."
                )

            html = path.read_text(encoding="utf-8")

        # HTTP/HTTPS webpage
        elif parsed.scheme in ("http", "https"):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text

        else:
            return f"Read error: unsupported URL scheme '{parsed.scheme}'."

        # Remove script and style blocks
        html = re.sub(
            r"<script.*?</script>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        html = re.sub(
            r"<style.*?</style>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", html)

        # Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Limit output size
        return text[:max_chars]

    except requests.RequestException as error:
        return f"Read error: {error}"

    except Exception as error:
        return f"Read error: {error}"


# -----------------------------
# Tool registry
# -----------------------------

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "read_webpage": read_webpage,
}


# -----------------------------
# Tool schemas for the LLM
# -----------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a simple arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression such as 12000 + 18000",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Read text from a local HTML file or webpage URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Local HTML filename or webpage URL",
                    }
                },
                "required": ["url"],
            },
        },
    },
]
