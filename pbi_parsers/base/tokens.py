from typing import Any


class BaseToken:
    tok_type: Any
    text: str

    def __init__(self, tok_type: Any, text: str) -> None:
        self.tok_type = tok_type
        self.text = text

    def __repr__(self) -> str:
        pretty_text = self.text.replace("\n", "\\n").replace("\r", "\\r")
        return f"Token(type={self.tok_type.name}, text='{pretty_text}')"
