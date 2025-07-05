from pbi_parsers.base import BaseScanner

from .tokens import KEYWORD_MAPPING, Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]


class Scanner(BaseScanner):
    def scan(self) -> tuple[Token]:
        return super().scan()  # type: ignore[override]

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if not self.peek():
            return Token(tok_type=TokenType.EOF, text="")

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
            return Token(
                tok_type=TokenType.WHITESPACE,
                text=self.source[start_pos : self.current_position],
            )
        if self.match("var", case_insensitive=True):
            return Token(
                tok_type=TokenType.VARIABLE,
                text="var",
            )
        if self.match("return", case_insensitive=True):
            return Token(
                tok_type=TokenType.RETURN,
                text="return",
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

        if self.match("["):
            while self.match(lambda c: c != "]"):
                pass
            if self.match("]"):
                return Token(
                    tok_type=TokenType.BRACKETED_IDENTIFIER,
                    text=self.source[start_pos : self.current_position],
                )
            msg = "Unterminated bracketed identifier"
            raise ValueError(msg)

        if self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    tok_type=TokenType.STRING_LITERAL,
                    text=self.source[start_pos : self.current_position],
                )
            msg = "Unterminated string literal"
            raise ValueError(msg)
        if self.match("//") or self.match("--"):
            while self.match(lambda c: c not in {"\n", ""}):
                pass
            return Token(
                tok_type=TokenType.SINGLE_LINE_COMMENT,
                text=self.source[start_pos : self.current_position],
            )
        if self.match("/*"):
            if self.match("*") and self.match("/"):
                return Token(
                    tok_type=TokenType.MULTI_LINE_COMMENT,
                    text=self.source[start_pos : self.current_position],
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
                return Token(tok_type=token_type, text=char)

        msg = f"Unexpected character: {self.peek()} at position {self.current_position}"
        raise ValueError(msg)
