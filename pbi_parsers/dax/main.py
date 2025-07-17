from collections.abc import Iterable

from .exprs._base import Expression
from .formatter import Formatter
from .parser import Parser
from .scanner import Scanner
from .tokens import Token, TokenType


def remove_non_executing_tokens(tokens: Iterable[Token]) -> list[Token]:
    """Removes tokens that are not executed in the DAX expression.

    Args:
        tokens (Iterable[Token]): List of tokens to filter.

    Returns:
        list[Token]: Filtered list of tokens that are executed.

    """
    return list(
        filter(
            lambda x: x.tok_type
            not in {
                TokenType.WHITESPACE,
                TokenType.SINGLE_LINE_COMMENT,
                TokenType.MULTI_LINE_COMMENT,
            },
            tokens,
        ),
    )


def to_ast(text: str) -> Expression | None:
    """Converts a DAX expression string into an AST (Abstract Syntax Tree).

    Args:
        text (str): The DAX expression to parse.

    Returns:
        Expression | None: when matched, returns the root node of the AST representing the DAX expression.
            When not matched, returns None.

    """
    tokens = Scanner(text).scan()
    tokens = remove_non_executing_tokens(tokens)
    parser = Parser(tokens)
    return parser.to_ast()


def format_expression(text: str) -> str:
    """Formats a DAX expression string into a more readable format.

    Args:
        text (str): The DAX expression to format.

    Returns:
        str: The formatted DAX expression.

    """
    ast = to_ast(text)
    if ast is None:
        return text
    return Formatter(ast).format()
