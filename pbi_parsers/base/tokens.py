from dataclasses import dataclass, field
from typing import Any


@dataclass
class TextSlice:
    full_text: str = ""
    start: int = -1
    end: int = -1

    def get_text(self) -> str:
        """Returns the text slice."""
        return self.full_text[self.start : self.end]

    def __repr__(self) -> str:
        """Returns a string representation of the TextSlice."""
        return f"TextSlice(text='{self.get_text()}', start={self.start}, end={self.end})"


@dataclass
class BaseToken:
    tok_type: Any
    text_slice: TextSlice = field(default_factory=TextSlice)

    def __repr__(self) -> str:
        pretty_text = self.text_slice.get_text().replace("\n", "\\n").replace("\r", "\\r")
        return f"Token(type={self.tok_type.name}, text='{pretty_text}')"

    @property
    def text(self) -> str:
        """Returns the text of the token."""
        return self.text_slice.get_text()

    def position(self) -> tuple[int, int]:
        """Returns the start and end positions of the token."""
        return self.text_slice.start, self.text_slice.end
