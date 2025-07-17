from typing import TypeVar

from .exprs import Expression
from .tokens import Token

T = TypeVar("T", bound=Expression)


def find_all(ast: Expression, class_type: type[T]) -> list[T]:
    """Find all instances of a specific class type in the AST."""
    ret = []
    for child in ast.children():
        if isinstance(child, class_type):
            ret.append(child)
        ret.extend(find_all(child, class_type))
    return ret


def highlight_section(node: Expression | Token):
    position = node.position()
    if isinstance(node, Expression):
        text = 1
