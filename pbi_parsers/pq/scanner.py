import string

from pbi_parsers.base import BaseScanner

from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("null", "true", "false")


class Scanner(BaseScanner):
    def scan(self) -> tuple[Token]:
        return super().scan()  # type: ignore[override]

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if not self.peek():
            return Token(tok_type=TokenType.EOF, text="")

        # TODO: handle as a builtin?
        for c in ("int64.type", "currency.type"):
            if self.match(c, case_insensitive=True):
                return Token(
                    tok_type=TokenType.TYPE_LITERAL,
                    text=c,
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
                    return Token(tok_type=token_type, text=name)
                # if the next character is an alpha character, it is not a keyword
                # but an identifier, so we need to backtrack
                self.advance(-len(name))

        # keywords have to be checked after the above tokens because "null" blocks "nullable"
        for keyword in KEYWORDS:
            if self.match(keyword, case_insensitive=True):
                return Token(
                    tok_type=TokenType.KEYWORD,
                    text=keyword,
                )

        if self.match('#"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    tok_type=TokenType.HASH_IDENTIFIER,
                    text=self.source[start_pos : self.current_position],
                )
            msg = f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
            raise ValueError(msg)

        if self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    tok_type=TokenType.STRING_LITERAL,
                    text=self.source[start_pos : self.current_position],
                )
            msg = f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
            raise ValueError(msg)

        if self.match("'"):
            while self.match(lambda c: c != "'"):
                pass
            if self.match("'"):
                return Token(
                    tok_type=TokenType.SINGLE_QUOTED_IDENTIFIER,
                    text=self.source[start_pos : self.current_position],
                )
            msg = "Unterminated string literal"
            raise ValueError(msg)

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return Token(
                tok_type=TokenType.WHITESPACE,
                text=self.source[start_pos : self.current_position],
            )
        if self.match("..."):
            return Token(
                tok_type=TokenType.ELLIPSIS,
                text="...",
            )

        if self.match("."):
            # must come before number literal to avoid conflict
            return Token(
                tok_type=TokenType.PERIOD,
                text=".",
            )

        if self.match(
            lambda c: c.isdigit() or c == ".",
        ):  # must come before unquoted identifier to avoid conflict
            while self.match(lambda c: c.isdigit() or c == "."):
                pass
            return Token(
                tok_type=TokenType.NUMBER_LITERAL,
                text=self.source[start_pos : self.current_position],
            )

        if self.match(lambda c: c.isalnum() or c == "_"):
            while self.match(lambda c: c.isalnum() or c == "_"):
                pass
            return Token(
                tok_type=TokenType.UNQUOTED_IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        if self.match("#"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return Token(
                tok_type=TokenType.HASH_IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        if self.match("//") or self.match("--"):
            while self.match(lambda c: c not in {"\n", ""}):
                pass
            return Token(
                tok_type=TokenType.SINGLE_LINE_COMMENT,
                text=self.source[start_pos : self.current_position],
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
                return Token(tok_type=token_type, text=char)

        print("---------------------")
        print(self.remaining())
        print("---------------------")
        breakpoint()
        msg = f"Unexpected character '{self.peek()}' at position {self.current_position}"
        raise ValueError(msg)
