from dataclasses import dataclass

from pbi_parsers.pq.exprs.function import FunctionExpression
from pbi_parsers.pq.exprs.literal_string import LiteralStringExpression


@dataclass
class ODataFeedSource:
    url: str | None = None

    @staticmethod
    def from_node(node: FunctionExpression) -> "ODataFeedSource":
        assert node.name.name() == "OData.Feed"
        url = node.args[0]
        if isinstance(url, LiteralStringExpression):
            return ODataFeedSource(url=url.value.text.strip('"'))
        return ODataFeedSource()
