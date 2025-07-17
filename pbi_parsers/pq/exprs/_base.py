from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class Expression:
    def pprint(self) -> str:
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @classmethod
    def match(cls, parser: "Parser") -> "Expression | None":
        """Attempt to match the current tokens to this expression type.

        Returns an instance of the expression if matched, otherwise None.
        """
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    @staticmethod
    def match_tokens(parser: "Parser", match_tokens: list[TokenType]) -> bool:
        return all(parser.peek(i).tok_type == token_type for i, token_type in enumerate(match_tokens))

    def __repr__(self) -> str:
        return self.pprint()
