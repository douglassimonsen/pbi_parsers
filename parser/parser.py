from typing import Final, Iterable

from .exprs import AddSubExpression, Expression, FunctionExpression, VariableExpression
from .tokens import Token, TokenType


class Parser:
    __tokens: Final[list[Token]]
    index: int = 0

    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.index = 0

    def peek(self, forward: int = 0) -> Token:
        """
        Peek at the next token without advancing the index.
        :param forward: How many tokens to look ahead.
        :return: The token at the current index + forward.
        """
        if self.index + forward >= len(self.__tokens):
            return Token(type=TokenType.EOF, text="")
        return self.__tokens[self.index + forward]

    def to_ast(self) -> Expression | None:
        """
        Parse the tokens and return the root expression.
        """
        return VariableExpression.match(self)
        return FunctionExpression.match(self)
        return AddSubExpression.match(self)

    def consume(self) -> Token:
        """Returns the next token and advances the index."""
        ret = self.__tokens[self.index]
        self.index += 1
        return ret

    def __bool__(self) -> bool:
        return self.index < len(self.__tokens)

    def __iter__(self) -> Iterable[Token]:
        return self.__tokens.__iter__()
