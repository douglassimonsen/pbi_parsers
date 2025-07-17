from collections.abc import Callable

from .tokens import BaseToken

MAX_POSITION = 1_000_000


class BaseLexer:
    source: str
    start_position: int
    current_position: int
    tokens: list[BaseToken]

    def __init__(self, source: str) -> None:
        self.source = source
        self.start_position = 0
        self.current_position = 0
        self.tokens = []

    def scan_helper(self) -> BaseToken:
        msg = "Subclasses should implement match_tokens method."
        raise NotImplementedError(msg)

    def match(
        self,
        matcher: Callable[[str], bool] | str,
        chunk: int = 1,
        *,
        case_insensitive: bool = True,
    ) -> bool:
        """Match a string or a callable matcher against the current position in the source.

        Args:
        ----
            matcher (Callable[[str], bool] | str): A string to match or a callable that
                takes a string and returns a boolean.
            chunk (int): The number of characters to check from the current position.
            case_insensitive (bool): If True, perform a case-insensitive match __only__ for strings.

        """
        if isinstance(matcher, str):
            chunk = len(matcher)

        string_chunk = self.peek(chunk)
        if not string_chunk:
            return False

        if isinstance(matcher, str):
            if case_insensitive:
                string_chunk = string_chunk.lower()
                matcher = matcher.lower()
            if string_chunk == matcher:
                self.advance(chunk)
                return True
            return False

        if matcher(string_chunk):
            self.advance(chunk)
            return True
        return False

    def peek(self, chunk: int = 1) -> str:
        return (
            self.source[self.current_position : self.current_position + chunk]
            if self.current_position < len(self.source)
            else ""
        )

    def remaining(self) -> str:
        return self.source[self.current_position :]

    def advance(self, chunk: int = 1) -> None:
        if self.current_position > MAX_POSITION:
            msg = f"Current position exceeds {MAX_POSITION:,} characters."
            raise ValueError(msg)
        self.current_position += chunk

    def scan(self) -> tuple[BaseToken, ...]:
        while not self.at_end():
            self.tokens.append(self.scan_helper())
        return tuple(self.tokens)

    def at_end(self) -> bool:
        return self.current_position >= len(self.source)
