from typing import TYPE_CHECKING, Any

from .tokens import Token, TokenType

if TYPE_CHECKING:
    from .exprs import Expression

EOF_TOKEN = Token()


class Parser:
    __tokens: list[Token]
    index: int = 0
    cache: dict[Any, Any]

    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.index = 0
        self.cache = {}

    def consume(self) -> Token:
        """Returns the next token and advances the index."""
        if self.index >= len(self.__tokens):
            return EOF_TOKEN
        ret = self.__tokens[self.index]
        self.index += 1
        return ret

    def peek(self, forward: int = 0) -> Token:
        """Peek at the next token without advancing the index.

        Args:
            forward (int): How many tokens to look ahead. Defaults to 0.

        Returns:
            Token: The token at the current index + forward.

        """
        if self.index + forward >= len(self.__tokens):
            return EOF_TOKEN
        return self.__tokens[self.index + forward]

    def remaining(self) -> list[Token]:
        """Returns the remaining tokens from the current index.

        Returns:
            list[Token]: The list of tokens from the current index to the end.

        """
        return self.__tokens[self.index :]

    def to_ast(self) -> "Expression | None":
        """Parse the tokens and return the root expression.

        Raises:
            ValueError: If no valid expression is found in the token stream.

        """
        from .exprs import any_expression_match  # noqa: PLC0415

        ret = any_expression_match(self)
        if ret is None:
            msg = "No valid expression found in the token stream."
            raise ValueError(msg)
        assert self.peek().tok_type == TokenType.EOF
        return ret
