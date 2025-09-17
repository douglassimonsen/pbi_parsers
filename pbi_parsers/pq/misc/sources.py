from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.main import to_ast

from .external_sources import ExcelWorkbookSource, JsonDocumentSource, ODataFeedSource
from .external_sources.csv_document import CsvDocumentSource
from .resolve import resolve_references

SOURCE_FUNCTIONS = {
    "Json.Document",
    "Csv.Document",
    "Sql.Database",
    "OData.Feed",
    "AzureStorage.Blobs",
    "AzureStorage.BlobContents",
    "Web.Contents",
    "Excel.Workbook",
}


def get_sources(text: str) -> list[str]:
    tree = to_ast(text)
    if tree is None:
        return []
    ret = []
    for node in tree.find_all(FunctionExpression):
        func_name = node.name.name()
        if func_name not in SOURCE_FUNCTIONS:
            continue
        resolved_node = resolve_references(node, tree)
        if func_name == "Excel.Workbook":
            ret.append(ExcelWorkbookSource.from_node(resolved_node))
        elif func_name == "Json.Document":
            ret.append(JsonDocumentSource.from_node(resolved_node))
        elif func_name == "OData.Feed":
            ret.append(ODataFeedSource.from_node(resolved_node))
        elif func_name == "Csv.Document":
            ret.append(CsvDocumentSource.from_node(resolved_node))
        else:
            breakpoint()
    return ret


# TODO: get the table of Excel.Workbook
# TODO: get columns of Json.Document
