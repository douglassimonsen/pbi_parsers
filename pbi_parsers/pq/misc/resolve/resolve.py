from typing import TYPE_CHECKING, Any

from pbi_parsers.pq.exprs import AddSubExpression, Expression, LiteralNumberExpression
from pbi_parsers.pq.exprs.concatenation import ConcatenationExpression
from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.identifier import IdentifierExpression
from pbi_parsers.pq.exprs.keyword import KeywordExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression
from pbi_parsers.pq.exprs.record import RecordExpression
from pbi_parsers.pq.exprs.variable import VariableExpression
from pbi_parsers.pq.tokens import Token

from .functions import resolve_binary_decompress, resolve_binary_from_text, resolve_json_document

if TYPE_CHECKING:
    from collections.abc import Callable


def to_number(val: str) -> float | int:
    try:
        return int(val)
    except ValueError:
        return float(val)


def add_sub_resolve(node: Expression, tree: Expression) -> AddSubExpression | LiteralNumberExpression:
    assert isinstance(node, AddSubExpression)
    resolve_left = resolve_references(node.left, tree)
    resolve_right = resolve_references(node.right, tree)
    if isinstance(resolve_left, LiteralNumberExpression) and isinstance(resolve_right, LiteralNumberExpression):
        left_val = to_number(resolve_left.value.text)
        right_val = to_number(resolve_right.value.text)
        if node.operator.text == "+":
            return LiteralNumberExpression(value=Token.from_str(str(left_val + right_val)))
        if node.operator.text == "-":
            return LiteralNumberExpression(value=Token.from_str(str(left_val - right_val)))
    return AddSubExpression(left=resolve_left, operator=node.operator, right=resolve_right)


def function_resolve(node: Expression, tree: Expression) -> Expression:
    assert isinstance(node, FunctionExpression)

    resolve_args = [resolve_references(arg, tree) for arg in node.args]
    resolved_function = FunctionExpression(name=node.name, args=resolve_args)
    func_name = node.name.name()
    if func_name == "Binary.Decompress":
        return resolve_binary_decompress(resolved_function)
    if func_name == "Binary.FromText":
        return resolve_binary_from_text(resolved_function)
    if func_name == "Json.Document":
        return resolve_json_document(resolved_function)
    return resolved_function


def concatenate_resolve(node: Expression, tree: Expression) -> Expression:
    assert isinstance(node, ConcatenationExpression)
    resolve_left = resolve_references(node.left, tree)
    resolve_right = resolve_references(node.right, tree)
    if isinstance(resolve_left, LiteralStringExpression) and isinstance(resolve_right, LiteralStringExpression):
        return LiteralStringExpression(
            value=Token.from_str(
                resolve_left.value.text[:-1] + resolve_right.value.text[1:],
            ),  # we remove the touching quotation marks
        )
    return ConcatenationExpression(left=resolve_left, right=resolve_right, operator=node.operator)


def record_resolve(node: Expression, tree: Expression) -> Expression:
    assert isinstance(node, RecordExpression)
    return RecordExpression(
        args=[(resolve_references(field[0], tree), resolve_references(field[1], tree)) for field in node.args],
    )


def resolve_references(node: Expression, tree: Expression) -> Any:
    """Resolve references in the given Power Query M code."""
    resolve_map: dict[type[Expression], Callable[[Expression, Expression], Expression]] = {
        AddSubExpression: add_sub_resolve,
        ConcatenationExpression: concatenate_resolve,
        FunctionExpression: function_resolve,
        LiteralNumberExpression: lambda n, _t: n,
        LiteralStringExpression: lambda n, _t: n,
        KeywordExpression: lambda n, _t: n,
        IdentifierExpression: lambda n, _t: n,
        RecordExpression: record_resolve,
        VariableExpression: lambda n, _t: n,
    }
    resolve_func = resolve_map[type(node)]
    return resolve_func(node, tree)
