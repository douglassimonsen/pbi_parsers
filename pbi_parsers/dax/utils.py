from typing import TypeVar

from colorama import Fore, Style

from .exprs import Expression
from .tokens import Token

T = TypeVar("T", bound=Expression)


def find_all(ast: Expression, class_type: type[T] | tuple[type[T], ...]) -> list[T]:
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
        full_text = node.text_slice.full_text
    else:
        full_text = node.full_text()

    lines = full_text.split("\n")
    starting_line = full_text.count("\n", 0, position[0]) + 1
    final_line = full_text.count("\n", 0, position[1]) + 1

    section_lines = lines[starting_line - 2 : final_line + 1]

    lines = []
    for i, section_line in enumerate(section_lines):
        if i in {0, len(section_lines) - 1}:
            lines.append(f"{starting_line + i} | {section_line}")
        else:
            lines.append(f"{Style.BRIGHT}{Fore.CYAN}{starting_line + i} |{Style.RESET_ALL} {section_line}")

    return "\n".join(lines)
