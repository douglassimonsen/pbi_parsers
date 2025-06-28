from typing import TYPE_CHECKING

from ..tokens import TokenType

if TYPE_CHECKING:
    from ..parser import Parser


class Expression:
    def pprint(self, depth: int = 0) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def match(cls, parser: "Parser") -> "Expression | None":
        """
        Attempt to match the current tokens to this expression type.
        Returns an instance of the expression if matched, otherwise None.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @staticmethod
    def match_tokens(parser: "Parser", match_tokens: list[TokenType]) -> bool:
        for i, token_type in enumerate(match_tokens):
            if parser.peek(i).type != token_type:
                return False
        return True

    def __repr__(self) -> str:
        return self.pprint(depth=0)
