"""calculate — evaluate an arithmetic expression safely.

Input : expression (str), e.g. "(2 + 3) * sqrt(16)"
Output: int | float — the numeric result.

Safety: this is NOT eval(). The expression is parsed with `ast` and only a
whitelist is interpreted: numbers, + - * / // % **, parentheses, unary
minus, the constants pi and e, and the functions abs, round, min, max,
sqrt. Anything else (names, attributes, calls outside the whitelist,
strings) raises ValueError with the offending fragment, so an agent can
correct itself. Exponents are bounded to prevent runaway computation.

Deterministic, no side effects, stdlib only.

Example:
    >>> calculate("(2 + 3) * sqrt(16)")
    20.0
"""

import ast
import math
import operator

_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_CONSTANTS = {"pi": math.pi, "e": math.e}
_FUNCTIONS = {"abs": abs, "round": round, "min": min, "max": max, "sqrt": math.sqrt}

_MAX_EXPONENT = 128
_MAX_POW_BASE = 10**9


def calculate(expression: str):
    """Evaluate `expression` and return its numeric result."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression {expression!r}: {exc.msg}") from None
    return _evaluate(tree.body)


def _evaluate(node: ast.AST):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError(f"Only numbers are allowed, got {node.value!r}")
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow):
            if abs(right) > _MAX_EXPONENT or abs(left) > _MAX_POW_BASE:
                raise ValueError(
                    f"Exponentiation out of bounds: {left} ** {right} "
                    f"(|exponent| <= {_MAX_EXPONENT}, |base| <= {_MAX_POW_BASE})"
                )
        return _BINARY[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(
            f"Unknown name {node.id!r}; allowed constants: "
            f"{', '.join(sorted(_CONSTANTS))}"
        )
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in _FUNCTIONS:
            if node.keywords:
                raise ValueError("Keyword arguments are not supported")
            return _FUNCTIONS[node.func.id](*[_evaluate(arg) for arg in node.args])
        name = getattr(node.func, "id", ast.dump(node.func))
        raise ValueError(
            f"Unknown function {name!r}; allowed functions: "
            f"{', '.join(sorted(_FUNCTIONS))}"
        )
    raise ValueError(f"Unsupported syntax: {ast.dump(node)[:80]}")
