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

    def advance(self, chunk: int = 1) -> None:
        """Advances the current position by the specified chunk size.

        Generally used alongside peek to consume characters.

        Args:
            chunk (int): The number of characters to advance the current position.

        Raises:
            ValueError: If the current position exceeds a predefined MAX_POSITION (1,000,000 characters).
                This is to avoid errors with the lexer causing the process to hang

        """
        if self.current_position > MAX_POSITION:
            msg = f"Current position exceeds {MAX_POSITION:,} characters."
            raise ValueError(msg)
        self.current_position += chunk

    def at_end(self) -> bool:
        """Checks if the current position is at (or beyond) the end of the source.

        Returns:
            bool: True if the current position is at or beyond the end of the source, False
                otherwise.

        """
        return self.current_position >= len(self.source)

    def match(
        self,
        matcher: Callable[[str], bool] | str,
        chunk: int = 1,
        *,
        case_insensitive: bool = True,
    ) -> bool:
        """Match a string or a callable matcher against the current position in the source.

        Args:
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
        """Returns the next section of text from the current position of length `chunk`. Defaults to a single character.

        Args:
            chunk (int): The number of characters to return from the current position.

        Returns:
            str: The next chunk of text from the current position.

        """
        return (
            self.source[self.current_position : self.current_position + chunk]
            if self.current_position < len(self.source)
            else ""
        )

    def remaining(self) -> str:
        """Returns the remaining text from the current position to the end of the source.

        Only used for testing and debugging purposes.

        Returns:
            str: The remaining text from the current position to the end of the source.

        """
        return self.source[self.current_position :]

    def scan(self) -> tuple[BaseToken, ...]:
        """Repeatedly calls scan_helper until the end of the source is reached.

        Returns:
            tuple[BaseToken, ...]: A tuple of tokens scanned from the source.

        """
        while not self.at_end():
            self.tokens.append(self.scan_helper())
        for a_tok, b_tok in zip(self.tokens, self.tokens[1:], strict=False):
            a_tok.next_token = b_tok
            b_tok.prior_token = a_tok
        return tuple(self.tokens)

    def scan_helper(self) -> BaseToken:
        """Contains the orchestration logic for converting tokens into expressions."""
        msg = "Subclasses should implement match_tokens method."
        raise NotImplementedError(msg)
