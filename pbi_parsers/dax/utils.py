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
{%- for i, section_line in enumerate(lines) -%}
{%- if i in highlights %}
{{ Style.BRIGHT }}{{ Fore.CYAN }}{{ i }} |{{ Style.RESET_ALL }} {{ section_line }}
{{ " " * (highlights[i][0]) }}{{ Style.BRIGHT }}{{ Fore.YELLOW }}{{ "^" * (highlights[i][1] - highlights[i][0]) }}{{ Style.RESET_ALL }}
{%- elif i >= section_boundary_lines[0] and i <= section_boundary_lines[1] %}
{{ i }} | {{ section_line }}
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
""")  # noqa: E501


class Context:
    position: tuple[int, int]
    full_text: str

    def __init__(self, position: tuple[int, int], full_text: str) -> None:
        self.position = position
        self.full_text = full_text

    def __repr__(self) -> str:
        return self.to_console()

    @staticmethod
    def _get_highlighted_text(
        lines: list[str],
        position: tuple[int, int],
    ) -> dict[int, tuple[int, int]]:
        highlight_line_dict: dict[int, tuple[int, int]] = {}

        remaining_start, remaining_end = position
        for i, line in enumerate(lines):
            if len(line) > remaining_start and remaining_end > 0:
                buffer = len(str(i)) + 3
                highlight_line_dict[i] = (
                    buffer + remaining_start,
                    buffer + min(remaining_end, len(line)),
                )
            remaining_start -= len(line) + 1  # +1 for the newline character
            remaining_end -= len(line) + 1
        return highlight_line_dict

    def to_console(self, context_lines: int = 2) -> str:
        """Render the context for console output."""
        lines = self.full_text.split("\n")
        starting_line = self.full_text.count("\n", 0, self.position[0])
        final_line = self.full_text.count("\n", 0, self.position[1])
        section_boundary_lines = (max(starting_line - context_lines, 0), min(final_line + context_lines, len(lines)))
        highlights = self._get_highlighted_text(lines, self.position)
        return CONSOLE.render(
            lines=lines,
            section_boundary_lines=section_boundary_lines,
            highlights=highlights,
            enumerate=enumerate,
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


def highlight_section(node: Expression | Token | list[Token] | list[Expression]) -> Context:
    if isinstance(node, list):
        position = (node[0].position()[0], node[-1].position()[1])
        first_node = node[0]
        full_text = first_node.text_slice.full_text if isinstance(first_node, Token) else first_node.full_text()
        return Context(position, full_text)

    position = node.position()
    full_text = node.text_slice.full_text if isinstance(node, Token) else node.full_text()
    return Context(position, full_text)
