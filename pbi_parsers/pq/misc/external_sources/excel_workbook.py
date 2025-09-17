from dataclasses import dataclass

from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression


@dataclass
class ExcelWorkbookSource:
    file: str | None = None
    table: str | None = None

    @staticmethod
    def from_node(node: FunctionExpression) -> "ExcelWorkbookSource":
        assert node.name.name() == "Excel.Workbook"

        return ExcelWorkbookSource(file=_get_file_path(node), table=None)


def _get_file_path(node: FunctionExpression) -> str | None:
    if len(node.args) < 1:
        return None
    first_arg = node.args[0]
    if not isinstance(first_arg, FunctionExpression):
        return None
    if first_arg.name.name() != "File.Contents":
        return None
    firster_arg = first_arg.args[0]
    if not isinstance(firster_arg, LiteralStringExpression):
        return None
    return firster_arg.value.text.strip('"')
