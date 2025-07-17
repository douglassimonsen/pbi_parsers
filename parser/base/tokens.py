from enum import Enum


class BaseTokenType(Enum):
    pass


class BaseToken:
    type: BaseTokenType
    text: str

    def __init__(self, type: BaseTokenType, text: str):
        self.type = type
        self.text = text

    def __repr__(self):
        pretty_text = self.text.replace("\n", "\\n").replace("\r", "\\r")
        return f"Token(type={self.type.name}, text='{pretty_text}')"
