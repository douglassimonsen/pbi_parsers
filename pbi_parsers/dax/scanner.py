from pbi_parsers.base import BaseScanner

from ..base.tokens import TextSlice
from .tokens import KEYWORD_MAPPING, Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]


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
        return Token(tok_type=tok_type, text=text_slice)

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if not self.peek():
            return Token(tok_type=TokenType.EOF, text=TextSlice())

        if self.match(
            "in ",
            case_insensitive=True,
        ):  # I have found no case where "in" is not followed by a space
            # this allows us to avoid matching with the "int" function
            return Token(
                tok_type=TokenType.IN,
                text="in",
            )

        for keyword, token_type in KEYWORD_MAPPING.items():
            if self.match(keyword, case_insensitive=True):
                return Token(
                    tok_type=token_type,
                    text=keyword,
                )

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return self.create_token(
                tok_type=TokenType.WHITESPACE,
                start_pos=start_pos,
            )
        if self.match("var", case_insensitive=True):
            return self.create_token(
                tok_type=TokenType.VARIABLE,
                start_pos=start_pos,
            )
        if self.match("return", case_insensitive=True):
            return self.create_token(
                tok_type=TokenType.RETURN,
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

        if self.match("["):
            while self.match(lambda c: c != "]"):
                pass
            if self.match("]"):
                return self.create_token(
                    tok_type=TokenType.BRACKETED_IDENTIFIER,
                    start_pos=start_pos,
                )
            msg = "Unterminated bracketed identifier"
            raise ValueError(msg)

        if self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return self.create_token(
                    tok_type=TokenType.STRING_LITERAL,
                    start_pos=start_pos,
                )
            msg = "Unterminated string literal"
            raise ValueError(msg)
        if self.match("//") or self.match("--"):
            while self.match(lambda c: c not in {"\n", ""}):
                pass
            return self.create_token(
                tok_type=TokenType.SINGLE_LINE_COMMENT,
                start_pos=start_pos,
            )
        if self.match("/*"):
            if self.match("*") and self.match("/"):
                return self.create_token(
                    tok_type=TokenType.MULTI_LINE_COMMENT,
                    start_pos=start_pos,
                )
            self.advance()
            msg = "Unterminated multi-line comment"
            raise ValueError(msg)

        fixed_character_mapping = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            ",": TokenType.COMMA,
            "==": TokenType.EQUAL_SIGN,
            "=": TokenType.EQUAL_SIGN,
            "{": TokenType.LEFT_CURLY_BRACE,
            "}": TokenType.RIGHT_CURLY_BRACE,
            "<>": TokenType.NOT_EQUAL_SIGN,
            "<=": TokenType.COMPARISON_OPERATOR,
            "<": TokenType.COMPARISON_OPERATOR,
            ">=": TokenType.COMPARISON_OPERATOR,
            ">": TokenType.COMPARISON_OPERATOR,
            "||": TokenType.DOUBLE_PIPE_OPERATOR,
            "&&": TokenType.DOUBLE_AMPERSAND_OPERATOR,
            "&": TokenType.AMPERSAND_OPERATOR,
            "+": TokenType.PLUS_SIGN,
            "-": TokenType.MINUS_SIGN,
            "^": TokenType.EXPONENTIATION_SIGN,
            "*": TokenType.MULTIPLY_SIGN,
            "%": TokenType.MODULUS_SIGN,
            "/": TokenType.DIVIDE_SIGN,
        }

        for char, token_type in fixed_character_mapping.items():
            if self.match(char):
                return self.create_token(tok_type=token_type, start_pos=start_pos)

        msg = f"Unexpected character: {self.peek()} at position {self.current_position}"
        raise ValueError(msg)
