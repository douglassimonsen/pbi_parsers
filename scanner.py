import string

from tokens import Token, TokenType


class Scanner:
    source: str
    start_position: int
    current_position: int
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.start_position = 0
        self.current_position = 0
        self.tokens = []

    def match(self, char: str) -> Token:
        pass

    def peek(self) -> str | None:
        return (
            self.source[self.current_position]
            if self.current_position < len(self.source)
            else None
        )

    def remaining(self) -> str:
        return self.source[self.current_position :]

    def advance(self) -> None:
        self.current_position += 1

    def scan_helper(self) -> Token:
        char = self.peek()
        if char is None:
            return Token(type=TokenType.EOF, text="")

        chars: list[str] = []
        if char in string.whitespace:
            while char is not None and char in string.whitespace:
                chars.append(char)
                self.advance()
                char = self.peek()
            return Token(type=TokenType.WHITESPACE, text="".join(chars))

        elif char in string.ascii_letters + "_":
            while char is not None and (
                char in string.ascii_letters + string.digits + "_"
            ):
                chars.append(char)
                self.advance()
                char = self.peek()
            return Token(type=TokenType.IDENTIFIER, text="".join(chars))

        elif char == "(":
            self.advance()
            return Token(type=TokenType.LEFT_PAREN, text="(")

        elif char == ")":
            self.advance()
            return Token(type=TokenType.RIGHT_PAREN, text=")")

        elif char == ",":
            self.advance()
            return Token(type=TokenType.COMMA, text=",")

        elif char == "=":
            self.advance()
            return Token(type=TokenType.EQUAL_SIGN, text="=")

        elif char == "'":
            chars.append("'")
            self.advance()
            char = self.peek()
            while char is not None and char != "'":
                chars.append(char)
                self.advance()
                char = self.peek()
            if char == "'":
                chars.append("'")
                self.advance()
                return Token(
                    type=TokenType.SINGLE_QUOTED_IDENTIFIER, text="".join(chars)
                )
            else:
                raise ValueError("Unterminated string literal")

        elif char == "[":
            chars.append("[")
            self.advance()
            char = self.peek()
            while char is not None and char != "]":
                chars.append(char)
                self.advance()
                char = self.peek()
            if char == "]":
                chars.append("]")
                self.advance()
                return Token(type=TokenType.BRACKETED_IDENTIFIER, text="".join(chars))
            else:
                raise ValueError("Unterminated bracketed identifier")

        elif char == '"':
            chars.append('"')
            self.advance()
            char = self.peek()
            while char is not None and char != '"':
                chars.append(char)
                self.advance()
                char = self.peek()
            if char == '"':
                chars.append('"')
                self.advance()
                return Token(type=TokenType.STRING_LITERAL, text="".join(chars))
            else:
                raise ValueError("Unterminated string literal")
        elif char == "/":
            # If / is being used as an operator, it will be handled in the next if block.
            chars.append("/")
            self.advance()
            char = self.peek()
            if char == "/":
                chars.append("/")
                self.advance()
                char = self.peek()
                while char is not None and char != "\n":
                    chars.append(char)
                    self.advance()
                    char = self.peek()
                return Token(type=TokenType.SINGLE_LINE_COMMENT, text="".join(chars))
            elif char == "*":
                chars.append("*")
                self.advance()
                char = self.peek()
                while char is not None:
                    if char == "*":
                        chars.append("*")
                        self.advance()
                        char = self.peek()
                        if char == "/":
                            chars.append("/")
                            self.advance()
                            return Token(
                                type=TokenType.MULTI_LINE_COMMENT, text="".join(chars)
                            )
                    else:
                        chars.append(char)
                        self.advance()
                        char = self.peek()
                raise ValueError("Unterminated multi-line comment")
            else:
                return Token(type=TokenType.OPERATOR, text="/")
        elif char in "+-*%&":
            # "/" is handled in the comment blocks above.
            chars.append(char)
            self.advance()
            return Token(type=TokenType.OPERATOR, text="".join(chars))
        elif char.isdigit():
            while char is not None and (char.isdigit() or char == "."):
                chars.append(char)
                self.advance()
                char = self.peek()
            return Token(type=TokenType.NUMBER_LITERAL, text="".join(chars))
        elif char == ".":
            self.advance()
            return Token(type=TokenType.PERIOD, text=".")
        elif char == "{":
            self.advance()
            return Token(type=TokenType.LEFT_CURLY_BRACE, text="{")
        elif char == "}":
            self.advance()
            return Token(type=TokenType.RIGHT_CURLY_BRACE, text="}")
        elif char == "<":
            self.advance()
            if self.peek() == "=":
                self.advance()
                return Token(type=TokenType.OPERATOR, text="<=")
            elif self.peek() == ">":
                self.advance()
                return Token(type=TokenType.OPERATOR, text="<>")
            return Token(type=TokenType.OPERATOR, text="<")
        elif char == ">":
            self.advance()
            if self.peek() == "=":
                self.advance()
                return Token(type=TokenType.OPERATOR, text=">=")
            return Token(type=TokenType.OPERATOR, text=">")
        elif char == "|":
            self.advance()
            if self.peek() == "|":
                self.advance()
                return Token(type=TokenType.OPERATOR, text="||")
            return Token(type=TokenType.OPERATOR, text="|")
        print(self.remaining())
        breakpoint()

    def scan(self) -> None:
        while not self.at_end():
            self.tokens.append(self.scan_helper())
            print(self.tokens[-1])

    def at_end(self) -> bool:
        return self.current_position >= len(self.source)
