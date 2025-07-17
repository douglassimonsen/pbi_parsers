from typing import Any, Final, Iterable

from .exprs import (
    Expression,
)
from .tokens import Token, TokenType

EOF_TOKEN = Token(type=TokenType.EOF, text="")


class Parser:
    __tokens: Final[list[Token]]
    index: int = 0
    cache: dict[Any, Any]

    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.index = 0
        self.cache = {}

    def peek(self, forward: int = 0) -> Token:
        """
        Peek at the next token without advancing the index.
        :param forward: How many tokens to look ahead.
        :return: The token at the current index + forward.
        """
        if self.index + forward >= len(self.__tokens):
            return EOF_TOKEN
        return self.__tokens[self.index + forward]

    def remaining(self) -> list[Token]:
        """
        Returns the remaining tokens from the current index.
        :return: A list of tokens from the current index to the end.
        """
        return self.__tokens[self.index :]

    def to_ast(self) -> Expression | None:
        """
        Parse the tokens and return the root expression.
        """
        from .exprs import any_expression_match

        ret = any_expression_match(self)
        if ret is None:
            raise ValueError("No valid expression found in the token stream.")
        assert self.peek().type == TokenType.EOF
        return ret

    def consume(self) -> Token:
        """Returns the next token and advances the index."""
        if self.index >= len(self.__tokens):
            return EOF_TOKEN
        ret = self.__tokens[self.index]
        self.index += 1
        return ret

    def __bool__(self) -> bool:
        return self.index < len(self.__tokens)

    def __iter__(self) -> Iterable[Token]:
        return self.__tokens.__iter__()
