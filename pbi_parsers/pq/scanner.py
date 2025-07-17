import string

from pbi_parsers.base import BaseScanner

from ..base.tokens import TextSlice
from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("null", "true", "false")


class Scanner(BaseScanner):
    def scan(self) -> tuple[Token]:
        return super().scan()  # type: ignore[override]

    def create_token(self, tok_type: TokenType, start_pos: int) -> Token:
        """Create a new token with the given type and text."""
        text_slice = TextSlice(
            text=self.source,
            start=start_pos,
            end=self.current_position,
        )
        return Token(tok_type=tok_type, text_slice=text_slice)

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if not self.peek():
            return Token()

        # TODO: handle as a builtin?
        for c in ("int64.type", "currency.type"):
            if self.match(c, case_insensitive=True):
                return self.create_token(
                    tok_type=TokenType.TYPE_LITERAL,
                    start_pos=start_pos,
                )

        for name, token_type in (
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
        ):
            if self.match(name, case_insensitive=True):
                if not self.peek().isalpha():
                    return self.create_token(tok_type=token_type, start_pos=start_pos)
                # if the next character is an alpha character, it is not a keyword
                # but an identifier, so we need to backtrack
                self.advance(-len(name))

        # keywords have to be checked after the above tokens because "null" blocks "nullable"
        for keyword in KEYWORDS:
            if self.match(keyword, case_insensitive=True):
                return self.create_token(tok_type=TokenType.KEYWORD, start_pos=start_pos)

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

        if self.match("'"):
            while self.match(lambda c: c != "'"):
                pass
            if self.match("'"):
                return self.create_token(
                    tok_type=TokenType.SINGLE_QUOTED_IDENTIFIER,
                    start_pos=start_pos,
                )
            msg = "Unterminated string literal"
            raise ValueError(msg)

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return self.create_token(
                tok_type=TokenType.WHITESPACE,
                start_pos=start_pos,
            )
        if self.match("..."):
            return self.create_token(
                tok_type=TokenType.ELLIPSIS,
                start_pos=start_pos,
            )

        if self.match("."):
            # must come before number literal to avoid conflict
            return self.create_token(
                tok_type=TokenType.PERIOD,
                start_pos=start_pos,
            )

        if self.match(
            lambda c: c.isdigit() or c == ".",
        ):  # must come before unquoted identifier to avoid conflict
            while self.match(lambda c: c.isdigit() or c == "."):
                pass
            return self.create_token(
                tok_type=TokenType.NUMBER_LITERAL,
                start_pos=start_pos,
            )

        if self.match(lambda c: c.isalnum() or c == "_"):
            while self.match(lambda c: c.isalnum() or c == "_"):
                pass
            return self.create_token(
                tok_type=TokenType.UNQUOTED_IDENTIFIER,
                start_pos=start_pos,
            )

        if self.match("#"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return self.create_token(
                tok_type=TokenType.HASH_IDENTIFIER,
                start_pos=start_pos,
            )

        if self.match("//") or self.match("--"):
            while self.match(lambda c: c not in {"\n", ""}):
                pass
            return self.create_token(
                tok_type=TokenType.SINGLE_LINE_COMMENT,
                start_pos=start_pos,
            )

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

        print("---------------------")
        print(self.remaining())
        print("---------------------")
        breakpoint()
        msg = f"Unexpected character '{self.peek()}' at position {self.current_position}"
        raise ValueError(msg)
