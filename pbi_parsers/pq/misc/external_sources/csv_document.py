from dataclasses import dataclass
from enum import Enum

from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.identifier import IdentifierExpression
from pbi_parsers.pq.exprs.literal_number import LiteralNumberExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression
from pbi_parsers.pq.exprs.record import RecordExpression

from .base import BaseSource
from .utils import PATHLIKE_FUNCTIONS


class CsvEncoding(Enum):
    UTF8 = 65001
    Windows = 1252


class QuoteStyle(Enum):
    None_ = "QuoteStyle.None"


def get_record_value(node: RecordExpression, key: str) -> str | int | float | None:
    for k, v in node.args:
        if isinstance(k, IdentifierExpression) and k.name() == key:
            if isinstance(v, LiteralStringExpression):
                return v.value.text.strip('"')
            if isinstance(v, LiteralNumberExpression):
                try:
                    return int(v.value.text)
                except ValueError:
                    return float(v.value.text)
            if isinstance(v, IdentifierExpression):
                return v.name()
    return None


@dataclass
class CsvDocumentSource(BaseSource):
    file_path: str | None = None
    delimiter: str | None = None
    column_count: int | None = None
    encoding_style: CsvEncoding | None = None
    quote_style: QuoteStyle | None = None

    @staticmethod
    def from_node(node: FunctionExpression) -> "CsvDocumentSource":
        return CsvDocumentSource(
            file_path=_get_file_path(node),
            delimiter=_get_delimiter(node),
            column_count=_get_column_count(node),
            encoding_style=_get_encoding_style(node),
            quote_style=_get_quote_style(node),
        )


def _get_quote_style(node: FunctionExpression) -> QuoteStyle | None:
    if not isinstance(node.args[1], RecordExpression):
        return None
    value = get_record_value(node.args[1], "QuoteStyle")
    if not isinstance(value, str):
        return None
    return QuoteStyle(value)


def _get_encoding_style(node: FunctionExpression) -> CsvEncoding | None:
    if not isinstance(node.args[1], RecordExpression):
        return None
    value = get_record_value(node.args[1], "Encoding")
    if not isinstance(value, int):
        return None
    return CsvEncoding(value)


def _get_column_count(node: FunctionExpression) -> int | None:
    if not isinstance(node.args[1], RecordExpression):
        return None
    value: str | int | float | None = get_record_value(node.args[1], "Columns")
    if not isinstance(value, int):
        return None
    return value


def _get_delimiter(node: FunctionExpression) -> str | None:
    if not isinstance(node.args[1], RecordExpression):
        return None
    value: str | int | float | None = get_record_value(node.args[1], "Delimiter")
    if not isinstance(value, str):
        return None
    return value


def _get_file_path(node: FunctionExpression) -> str | None:
    if len(node.args) < 1:
        return None
    first_arg = node.args[0]
    if not isinstance(first_arg, FunctionExpression):
        return None
    if first_arg.name.name() not in PATHLIKE_FUNCTIONS:
        return None
    firster_arg = first_arg.args[0]
    if not isinstance(firster_arg, LiteralStringExpression):
        return None
    return firster_arg.value.text.strip('"')
