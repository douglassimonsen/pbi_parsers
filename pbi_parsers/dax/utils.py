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


# TODO: adding ^^^ below a subsection,
# TODO: handle beginning at an offset, dedenting the section to start with the first non-space
# TODO: handle when the beginning starts in the middle of a line
def highlight_section(node: Expression | Token):
    position = node.position()
    if isinstance(node, Token):
        section = node.text_slice.full_text[position[0] : position[1]]
    else:
        section = node.full_text()[position[0] : position[1]]
    return f"{section} {position}"
