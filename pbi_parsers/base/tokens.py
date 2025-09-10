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
    prior_token: "BaseToken | None" = field(repr=False, default=None)
    next_token: "BaseToken | None" = field(repr=False, default=None)

    def __eq__(self, other: object) -> bool:
        """Checks equality based on token type and text slice."""
        if not isinstance(other, BaseToken):
            return NotImplemented
        return self.tok_type == other.tok_type and self.text_slice == other.text_slice

    def __hash__(self) -> int:
        """Returns a hash based on token type and text slice."""
        return hash((self.tok_type, self.text_slice))

    def __repr__(self) -> str:
        pretty_text = self.text_slice.get_text().replace("\n", "\\n").replace("\r", "\\r")
        return f"Token(type={self.tok_type.name}, text='{pretty_text}')"

    def position(self) -> tuple[int, int]:
        """Returns the start and end positions of the token.

        Returns:
            tuple[int, int]: A tuple containing the start and end positions of the token within the source text.

        """
        return self.text_slice.start, self.text_slice.end

    @property
    def text(self) -> str:
        """Returns the text underlying the token.

        Returns:
            str: The text of the token as a string.

        """
        return self.text_slice.get_text()

    def add_token_before(self, text: str, tok_type: Any) -> None:
        """Adds a token before the current token in the linked list.

        Args:
            text (str): The text to add before the current token.
            tok_type (Any): The type of the token to add.

        """
        new_global_text = (
            self.text_slice.full_text[: self.text_slice.start]
            + text
            + self.text_slice.full_text[self.text_slice.start :]
        )
        self._update_full_text(new_global_text)

        length = len(text)
        tok = BaseToken(
            tok_type=tok_type,
            text_slice=TextSlice(
                full_text=new_global_text,
                start=self.text_slice.start,
                end=self.text_slice.start + length,
            ),
            prior_token=self.prior_token,
            next_token=self,
        )
        if self.prior_token:
            self.prior_token.next_token = tok
        self.prior_token = tok

        # prior_token because we need to update the current token's position as well
        curr_tok = self.prior_token
        while curr_tok := curr_tok.next_token:
            curr_tok.text_slice.start += length
            curr_tok.text_slice.end += length

    def add_token_after(self, text: str, tok_type: Any) -> None:
        """Adds a token after the current token in the linked list.

        Args:
            text (str): The text to add before the current token.
            tok_type (Any): The type of the token to add.

        """
        new_global_text = (
            self.text_slice.full_text[: self.text_slice.end] + text + self.text_slice.full_text[self.text_slice.end :]
        )
        self._update_full_text(new_global_text)

        length = len(text)
        tok = BaseToken(
            tok_type=tok_type,
            text_slice=TextSlice(
                full_text=new_global_text,
                start=self.text_slice.end,
                end=self.text_slice.end + length,
            ),
            prior_token=self,
            next_token=self.next_token,
        )
        if self.next_token:
            self.next_token.prior_token = tok
        self.next_token = tok

        # prior_token because we need to update the current token's position as well
        curr_tok = self
        while curr_tok := curr_tok.next_token:
            curr_tok.text_slice.start += length
            curr_tok.text_slice.end += length

    def remove(self) -> None:
        """Removes the current token from the linked list."""
        new_global_text = (
            self.text_slice.full_text[: self.text_slice.start] + self.text_slice.full_text[self.text_slice.end :]
        )
        self._update_full_text(new_global_text)

        curr_tok = self
        length = len(self.text)
        while curr_tok := curr_tok.next_token:
            curr_tok.text_slice.start -= length
            curr_tok.text_slice.end -= length

        if self.prior_token:
            self.prior_token.next_token = self.next_token
        if self.next_token:
            self.next_token.prior_token = self.prior_token
        self.prior_token = None
        self.next_token = None

    def replace(self, new_text: str) -> None:
        """Replaces the text of the current token with new text.

        Args:
            new_text (str): The new text to replace the current token's text.

        """
        new_global_text = (
            self.text_slice.full_text[: self.text_slice.start]
            + new_text
            + self.text_slice.full_text[self.text_slice.end :]
        )
        self._update_full_text(new_global_text)

        len_diff = len(new_text) - len(self.text)
        # Adjust the positions of subsequent tokens
        self.text_slice.end += len_diff
        current = self.next_token
        while current:
            current.text_slice.start += len_diff
            current.text_slice.end += len_diff
            current = current.next_token

    def _update_full_text(self, new_full_text: str) -> None:
        """Updates the full text of the token and adjusts the text slice accordingly.

        Args:
            new_full_text (str): The new full text to update the token's text slice.

        """
        self.text_slice.full_text = new_full_text
        curr_tok = self
        while curr_tok := curr_tok.next_token:
            curr_tok.text_slice.full_text = new_full_text
        curr_tok = self
        while curr_tok := curr_tok.prior_token:
            curr_tok.text_slice.full_text = new_full_text
