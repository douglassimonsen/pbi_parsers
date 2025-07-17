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


class LiteralStringExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f"LiteralString ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, tokens: list[Token]) -> "LiteralStringExpression | None":
        if cls.match_tokens(tokens, [TokenType.STRING_LITERAL]):
            value = tokens.pop(0)
            return LiteralStringExpression(value=value)


class LiteralNumberExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f"LiteralNumber ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, tokens: list[Token]) -> "LiteralNumberExpression | None":
        if cls.match_tokens(tokens, [TokenType.NUMBER_LITERAL]):
            value = tokens.pop(0)
            return LiteralNumberExpression(value=value)


class MeasureExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self, depth: int = 0) -> str:
        base = f"Measure ({self.name.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, tokens: list[Token]) -> "MeasureExpression | None":
        if cls.match_tokens(tokens, [TokenType.BRACKETED_IDENTIFIER]):
            name = tokens.pop(0)
            return MeasureExpression(name=name)


class FunctionExpression(Expression):
    def __init__(self, name: Token, args: list[Expression]):
        self.name = name
        self.args = args

    def pprint(self, depth: int = 0) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        base = f"""
Function (
    name: {self.name.text},
    args: {args}
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
            # We gotta handle operators next :(
            for expr in (
                ColumnExpression,
                MeasureExpression,
                FunctionExpression,
                LiteralStringExpression,
                LiteralNumberExpression,
            ):
                if arg := expr.match(tokens):
                    args.append(arg)
                    break
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
        if ret := MeasureExpression.match(tokens):
            return ret
        else:
            raise ValueError(f"Unexpected token sequence: {tokens[:3]}")
