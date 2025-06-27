import textwrap

from tokens import Token, TokenType


class Expression:
    def pprint(self, depth: int = 0) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def match(cls, tokens: list[Token]) -> "Expression | None":
        """
        Attempt to match the current tokens to this expression type.
        Returns an instance of the expression if matched, otherwise None.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @staticmethod
    def match_tokens(tokens: list[Token], match_tokens: list[TokenType]) -> bool:
        for token, token_type in zip(tokens, match_tokens):
            if token.type != token_type:
                return False
        return True


class ColumnExpression(Expression):
    table: Token
    column: Token

    def __init__(self, table: Token, column: Token):
        self.table = table
        self.column = column

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Column (
    {self.table.text}, 
    {self.column.text}
)""".strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, tokens: list[Token]) -> "ColumnExpression | None":
        if cls.match_tokens(
            tokens, [TokenType.SINGLE_QUOTED_IDENTIFIER, TokenType.BRACKETED_IDENTIFIER]
        ):
            table, column = tokens.pop(0), tokens.pop(0)
            return ColumnExpression(table=table, column=column)


class FunctionExpression(Expression):
    def __init__(self, name: Token, args: list[Expression]):
        self.name = name
        self.args = args

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Function (
    name: {self.name.text},
    args: 
    {", ".join(arg.pprint(depth + 1) for arg in self.args)}
)        """.strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, tokens: list[Token]) -> "FunctionExpression | None":
        if not cls.match_tokens(
            tokens, [TokenType.UNQUOTED_IDENTIFIER, TokenType.LEFT_PAREN]
        ):
            return None
        args: list[Expression] = []
        name, _paren = (
            tokens.pop(0),
            tokens.pop(0),
        )  # Skip the function name and left parenthesis
        while not cls.match_tokens(tokens, [TokenType.RIGHT_PAREN]):
            if arg := ColumnExpression.match(tokens):
                args.append(arg)
            elif arg := FunctionExpression.match(tokens):
                args.append(arg)
            else:
                breakpoint()
                raise ValueError(f"Unexpected token sequence: {tokens[:3]}")
            if not cls.match_tokens(tokens, [TokenType.RIGHT_PAREN]):
                assert cls.match_tokens(tokens, [TokenType.COMMA]), (
                    f"Expected a comma, found: {tokens[:3]}"
                )
                tokens.pop(0)
        _right_paren = tokens.pop(0)
        ret = FunctionExpression(name=name, args=args)
        return ret

    def __repr__(self) -> str:
        return f"""
Function (
    name: {self.name}
)
"""


def to_ast(tokens: list[Token]) -> Expression:
    """
    Convert a list of tokens into an abstract syntax tree (AST).
    """
    while tokens:
        if ret := ColumnExpression.match(tokens):
            return ret
        if ret := FunctionExpression.match(tokens):
            return ret

        else:
            raise ValueError(f"Unexpected token sequence: {tokens[:3]}")
