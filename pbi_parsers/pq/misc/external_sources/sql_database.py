from dataclasses import dataclass

from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression

from .base import BaseSource


@dataclass
class SqlDatabaseSource(BaseSource):
    server: str | None = None
    database: str | None = None

    @staticmethod
    def from_node(node: FunctionExpression) -> "SqlDatabaseSource":
        return SqlDatabaseSource(
            server=_get_server(node),
            database=_get_database(node),
        )


def _get_server(node: FunctionExpression) -> str | None:
    if len(node.args) < 1:
        return None
    first_arg = node.args[0]
    if not isinstance(first_arg, LiteralStringExpression):
        return None
    return first_arg.value.text.strip('"')


def _get_database(node: FunctionExpression) -> str | None:
    if len(node.args) < 2:  # noqa: PLR2004
        return None
    second_arg = node.args[1]
    if not isinstance(second_arg, LiteralStringExpression):
        return None
    return second_arg.value.text.strip('"')
