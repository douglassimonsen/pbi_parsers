from dataclasses import dataclass, field
from typing import Any


@dataclass
class TextSlice:
    full_text: str = ""
    start: int = -1
    end: int = -1

    def __eq__(self, other: object) -> bool:
        """Checks equality based on the text slice."""
        if not isinstance(other, TextSlice):
            return NotImplemented
        return self.full_text == other.full_text and self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        """Returns a hash based on the text slice."""
        return hash((self.full_text, self.start, self.end))

    def __repr__(self) -> str:
        """Returns a string representation of the TextSlice."""
        return f"TextSlice(text='{self.get_text()}', start={self.start}, end={self.end})"

    def get_text(self) -> str:
        """Returns the text slice."""
        return self.full_text[self.start : self.end]


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

    def __eq__(self, other: object) -> bool:
        """Checks equality based on token type and text slice."""
        if not isinstance(other, BaseToken):
            return NotImplemented
        return self.tok_type == other.tok_type and self.text_slice == other.text_slice

    def __hash__(self) -> int:
        """Returns a hash based on token type and text slice."""
        return hash((self.tok_type, self.text_slice))
