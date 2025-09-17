from dataclasses import dataclass

from pbi_parsers.dax.exprs.literal_number import LiteralNumberExpression
from pbi_parsers.pq.exprs.array import ArrayExpression
from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression


def get_value(node: LiteralStringExpression | LiteralNumberExpression) -> str | int | float:
    if isinstance(node, LiteralStringExpression):
        return node.value.text.strip('"')
    if isinstance(node, LiteralNumberExpression):
        try:
            return int(node.value.text)
        except ValueError:
            return float(node.value.text)
    msg = f"Expected LiteralStringExpression or LiteralNumberExpression, got {type(node)}"
    raise ValueError(msg)


@dataclass
class JsonDocumentSource:
    values: list[list[str | int | float]] | None = None
    columns: list[str] | None = None

    @staticmethod
    def from_node(node: FunctionExpression) -> "JsonDocumentSource":
        if not isinstance(node, ArrayExpression):
            return JsonDocumentSource()
        data = [
            [get_value(e) for e in row.elements if isinstance(e, (LiteralStringExpression, LiteralNumberExpression))]
            for row in node.elements
            if isinstance(row, ArrayExpression)
        ]
        return JsonDocumentSource(values=data)
