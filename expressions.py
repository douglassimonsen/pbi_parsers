import textwrap
from functools import partial

from tokens import Token, TokenType

# MAke a parser class with a pointer index


class Expression:
    def pprint(self, depth: int = 0) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def match(cls, tokens: list[Token]) -> "tuple[Expression | None, list[Token]]":
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

    def __repr__(self) -> str:
        return self.pprint(depth=0)


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
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[ColumnExpression | None, list[Token]]":
        tokens = tokens[:]
        if cls.match_tokens(
            tokens, [TokenType.SINGLE_QUOTED_IDENTIFIER, TokenType.BRACKETED_IDENTIFIER]
        ):
            table, column = tokens.pop(0), tokens.pop(0)
            return ColumnExpression(table=table, column=column), tokens


class LiteralStringExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f"LiteralString ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[LiteralStringExpression | None, list[Token]]":
        if cls.match_tokens(tokens, [TokenType.STRING_LITERAL]):
            value = tokens.pop(0)
            return LiteralStringExpression(value=value)


class LiteralNumberExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f"Number ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[LiteralNumberExpression | None, list[Token]]":
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
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[MeasureExpression | None, list[Token]]":
        if cls.match_tokens(tokens, [TokenType.BRACKETED_IDENTIFIER]):
            name = tokens.pop(0)
            return MeasureExpression(name=name)


class FunctionExpression(Expression):
    name: Token
    args: list[Expression]

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
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[FunctionExpression | None, list[Token]]":
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


def or_match(
    exprs: tuple[type[Expression], ...], tokens: list[Token]
) -> Expression | None:
    """
    Match non-operator expressions like Column, Measure, Function, LiteralString, and LiteralNumber.
    """
    for expr in exprs:
        if ret := expr.match(tokens):
            return ret
    return None


div_mul_match = partial(
    or_match,
    exprs=(
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
    ),
)


class DivMulExpression(Expression):
    """
    Represents an multiplication or division expression.
    """

    operator: Token
    left: Expression
    right: Expression

    def __init__(self, operator: Token, left: Expression, right: Expression):
        self.operator = operator
        self.left = left
        self.right = right

    @classmethod
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[DivMulExpression | None, list[Token]]":
        left_term = div_mul_match(tokens=tokens)
        if not left_term:
            return None
        if not cls.match_tokens(tokens, [TokenType.OPERATOR]):
            return None
        if tokens[0].text not in ("*", "/"):
            return None
        operator = tokens.pop(0)
        right_term = div_mul_match(tokens=tokens)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {tokens[:3]}"
            )
        return DivMulExpression(
            operator=operator, left=left_term, right=right_term
        ), tokens

    def pprint(self, depth: int = 0) -> str:
        if self.operator.text == "*":
            op_str = "Mul"
        else:
            op_str = "Div"
        left_str = textwrap.indent(self.left.pprint(), " " * 10)[10:]
        right_str = textwrap.indent(self.right.pprint(), " " * 10)[10:]
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)"""


add_sub_match = partial(
    or_match,
    exprs=(
        DivMulExpression,
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
    ),
)


class AddSubExpression(Expression):
    """
    Represents an addition or subtraction expression.
    """

    operator: Token
    left: Expression
    right: Expression

    def __init__(self, operator: Token, left: Expression, right: Expression):
        self.operator = operator
        self.left = left
        self.right = right

    @classmethod
    def match(
        cls, tokens: list[Token]
    ) -> "tuple[AddSubExpression | None, list[Token]]":
        left_term = add_sub_match(tokens=tokens)
        if not left_term:
            return None
        if not cls.match_tokens(tokens, [TokenType.OPERATOR]):
            return None
        if tokens[0].text not in ("+", "-"):
            return None
        operator = tokens.pop(0)
        right_term = add_sub_match(tokens=tokens)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {tokens[:3]}"
            )
        return DivMulExpression(operator=operator, left=left_term, right=right_term)

    def __repr__(self, depth: int = 0) -> str:
        if self.operator.text == "+":
            op_str = "Add"
        else:
            op_str = "Sub"
        left_str = self.left.pprint(depth + 1)
        right_str = self.right.pprint(depth + 1)
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)"""


def to_ast(tokens: list[Token]) -> Expression:
    """
    Convert a list of tokens into an abstract syntax tree (AST).
    """
    while tokens:
        if ret := AddSubExpression.match(tokens):
            return ret
        exit()
        if ret := DivMulExpression.match(tokens):
            return ret
        if ret := ColumnExpression.match(tokens):
            return ret
        if ret := FunctionExpression.match(tokens):
            return ret
        if ret := MeasureExpression.match(tokens):
            return ret
        else:
            raise ValueError(f"Unexpected token sequence: {tokens[:3]}")
