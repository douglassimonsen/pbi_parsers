import string

from pbi_parsers.base import BaseLexer
from pbi_parsers.base.tokens import TextSlice

from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("null", "true", "false")
RESERVED_WORDS = (
    ("type", TokenType.TYPE),
    ("let", TokenType.LET),
    ("if", TokenType.IF),
    ("then", TokenType.THEN),
    ("else", TokenType.ELSE),
    ("each", TokenType.EACH),
    ("meta", TokenType.META),
    ("nullable", TokenType.NULLABLE),
    ("try", TokenType.TRY),
    ("otherwise", TokenType.OTHERWISE),
    ("and", TokenType.AND),
    ("or", TokenType.OR),
    ("not", TokenType.NOT),
    ("in", TokenType.IN),
    ("is", TokenType.IS),
    ("as", TokenType.AS),
)


class Lexer(BaseLexer):
    def scan(self) -> tuple[Token]:
        return super().scan()  # type: ignore[override]

    def create_token(self, tok_type: TokenType, start_pos: int) -> Token:
        """Create a new token with the given type and text."""
        text_slice = TextSlice(
            full_text=self.source,
            start=start_pos,
            end=self.current_position,
        )
        return Token(tok_type=tok_type, text_slice=text_slice)

    def _match_type_literal(self, start_pos: int) -> Token | None:
        for c in ("int64.type", "currency.type"):
            if self.match(c, case_insensitive=True):
                return self.create_token(
                    tok_type=TokenType.TYPE_LITERAL,
                    start_pos=start_pos,
                )
        return None

    def _match_reserved_words(self, start_pos: int) -> Token | None:
        for name, token_type in RESERVED_WORDS:
            if self.match(name, case_insensitive=True):
                if not self.peek().isalpha():
                    return self.create_token(tok_type=token_type, start_pos=start_pos)
                # if the next character is an alpha character, it is not a keyword
                # but an identifier, so we need to backtrack
                self.advance(-len(name))
        return None

    def _match_keyword(self, start_pos: int) -> Token | None:
        for keyword in KEYWORDS:
            if self.match(keyword, case_insensitive=True):
                return self.create_token(tok_type=TokenType.KEYWORD, start_pos=start_pos)
        return None

    def _match_hash_identifier(self, start_pos: int) -> Token | None:
        if self.match('#"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return self.create_token(
                    tok_type=TokenType.HASH_IDENTIFIER,
                    start_pos=start_pos,
                )
            msg = f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
            raise ValueError(msg)

        if self.match("#"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return self.create_token(
                tok_type=TokenType.HASH_IDENTIFIER,
                start_pos=start_pos,
            )

        return None

    def _match_string_literal(self, start_pos: int) -> Token | None:
        if self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return self.create_token(
                    tok_type=TokenType.STRING_LITERAL,
                    start_pos=start_pos,
                )
            msg = f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
            raise ValueError(msg)

        return None

    def _match_whitespace(self, start_pos: int) -> Token | None:
        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return self.create_token(
                tok_type=TokenType.WHITESPACE,
                start_pos=start_pos,
            )
        return None

    def _match_ellipsis(self, start_pos: int) -> Token | None:
        if self.match("..."):
            return self.create_token(
                tok_type=TokenType.ELLIPSIS,
                start_pos=start_pos,
            )
        return None

    def _match_period(self, start_pos: int) -> Token | None:
        if self.match("."):
            return self.create_token(
                tok_type=TokenType.PERIOD,
                start_pos=start_pos,
            )
        return None

    def _match_number_literal(self, start_pos: int) -> Token | None:
        if self.match(
            lambda c: c.isdigit() or c == ".",
        ):  # must come before unquoted identifier to avoid conflict
            while self.match(lambda c: c.isdigit() or c in {".", "e", "E"}):
                pass
            return self.create_token(
                tok_type=TokenType.NUMBER_LITERAL,
                start_pos=start_pos,
            )
        return None

    def _match_unquoted_identifier(self, start_pos: int) -> Token | None:
        if self.match(lambda c: c.isalnum() or c == "_"):
            while self.match(lambda c: c.isalnum() or c == "_"):
                pass
            return self.create_token(
                tok_type=TokenType.UNQUOTED_IDENTIFIER,
                start_pos=start_pos,
            )
        return None

    def _match_single_line_comment(self, start_pos: int) -> Token | None:
        if self.match("//") or self.match("--"):
            while self.match(lambda c: c not in {"\n", ""}):
                pass
            return self.create_token(
                tok_type=TokenType.SINGLE_LINE_COMMENT,
                start_pos=start_pos,
            )
        return None

    def _match_token(self, start_pos: int) -> Token | None:
        fixed_character_mapping = {
            "=>": TokenType.LAMBDA_ARROW,
            ">=": TokenType.COMPARISON_OPERATOR,
            "=": TokenType.EQUAL_SIGN,
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_CURLY_BRACE,
            "}": TokenType.RIGHT_CURLY_BRACE,
            ",": TokenType.COMMA,
            "[": TokenType.LEFT_BRACKET,
            "]": TokenType.RIGHT_BRACKET,
            "<>": TokenType.NOT_EQUAL_SIGN,
            "+": TokenType.PLUS_SIGN,
            "-": TokenType.MINUS_SIGN,
            "*": TokenType.MULTIPLY_SIGN,
            "/": TokenType.DIVIDE_SIGN,
            ">": TokenType.COMPARISON_OPERATOR,
            "&": TokenType.CONCATENATION_OPERATOR,
            "!": TokenType.EXCLAMATION_POINT,
        }

        for char, token_type in fixed_character_mapping.items():
            if self.match(char):
                return self.create_token(
                    tok_type=token_type,
                    start_pos=start_pos,
                )
        return None

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if not self.peek():
            return Token()

        for candidate_func in (
            self._match_type_literal,
            self._match_reserved_words,
            # keywords have to be checked after the above tokens because "null" blocks "nullable"
            self._match_keyword,
            self._match_hash_identifier,
            self._match_string_literal,
            self._match_whitespace,
            self._match_ellipsis,
            self._match_period,
            self._match_number_literal,
            self._match_unquoted_identifier,
            self._match_hash_identifier,
            self._match_single_line_comment,
            self._match_token,
        ):
            match_candidate = candidate_func(start_pos)
            if match_candidate:
                return match_candidate

        msg = f"Unexpected character '{self.peek()}' at position {self.current_position}"
        raise ValueError(msg)
