import token
from typing import Final

from tokens import Token, TokenType


class Parser:
    tokens: Final[list[Token]]
    token_index: int = 0

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def peek(self, offset: int = 0) -> Token:
        return self.tokens[self.token_index + offset]

    def consume(self, token_type: TokenType, error_message: str) -> Token:
        candidate_token = self.peek()
        if candidate_token.type != token_type:
            raise ValueError(f"{error_message} Expected {token_type.name}, got {candidate_token.type.name} at index {self.token_index}.")
        self.token_index += 1
        return candidate_token

    def match(self, token_types: list[TokenType]) -> bool:
        for i, token_type in enumerate(token_types):
            if self.token_index + i >= len(self.tokens):
                return False
            if self.tokens[self.token_index + i].type != token_type:
                return False
        return True

    def function_expr(self):
        if not self.match([TokenType.UNQUOTED_IDENTIFIER, TokenType.LEFT_PAREN]):
            return None
        while not self.match([TokenType.RIGHT_PAREN]):
            # Handle function arguments here
            pass

    def mult_div_expr(self):
        pass

    def parse(self) -> None: