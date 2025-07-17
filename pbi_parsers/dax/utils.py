from typing import TypeVar

import jinja2
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


CONSOLE = jinja2.Template("""
{%- for i, section_line in enumerate(section_lines) -%}
{%- if i == 0 or i == section_lines|length - 1 %}
{{ starting_line + i }} | {{ section_line }}
{%- else %}
{{ Style.BRIGHT }}{{ Fore.CYAN }}{{ starting_line + i }} |{{ Style.RESET_ALL }} {{ section_line }}
{%- endif %}
{%- endfor %}
""")
HTML = jinja2.Template("""
<div>
{% for i, section_line in enumerate(section_lines) %}
    <span class="{{ "" if i == 0 or i == section_lines|length - 1 else "highlighted" }}">{{ starting_line + i }} |</span>
    <span>{{ section_line }}</span>
{% endfor %}
<div>
""")


class Context:
    position: tuple[int, int]
    full_text: str

    def __init__(self, position: tuple[int, int], full_text: str) -> None:
        self.position = position
        self.full_text = full_text

    def __repr__(self) -> str:
        return self.to_console()

    def to_console(self) -> str:
        """Render the context for console output."""
        lines = self.full_text.split("\n")
        starting_line = self.full_text.count("\n", 0, self.position[0]) + 1
        final_line = self.full_text.count("\n", 0, self.position[1]) + 1

        section_lines = lines[starting_line - 2 : final_line + 1]
        return CONSOLE.render(
            section_lines=section_lines,
            enumerate=enumerate,
            starting_line=starting_line,
            Style=Style,
            Fore=Fore,
        )

    def to_dict(self) -> dict[str, str | tuple[int, int]]:
        """Convert the context to a dictionary."""
        return {
            "position": self.position,
            "full_text": self.full_text,
        }

    def to_html(self) -> str:
        """Render the context for console output."""
        lines = self.full_text.split("\n")
        starting_line = self.full_text.count("\n", 0, self.position[0]) + 1
        final_line = self.full_text.count("\n", 0, self.position[1]) + 1

        section_lines = lines[starting_line - 2 : final_line + 1]
        return HTML.render(
            section_lines=section_lines,
            enumerate=enumerate,
            starting_line=starting_line,
            Style=Style,
            Fore=Fore,
        )


# TODO: adding ^^^ below a subsection,
# TODO: handle beginning at an offset, dedenting the section to start with the first non-space
# TODO: handle when the beginning starts in the middle of a line
def highlight_section(node: Expression | Token | list[Token] | list[Expression]) -> Context:
    if isinstance(node, list):
        position = (node[0].position()[0], node[-1].position()[1])
        first_node = node[0]
        full_text = first_node.text_slice.full_text if isinstance(first_node, Token) else first_node.full_text()
        return Context(position, full_text)

    position = node.position()
    full_text = node.text_slice.full_text if isinstance(node, Token) else node.full_text()
    return Context(position, full_text)
