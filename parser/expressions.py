from parser.exprs._base import Expression
from parser.parser import Parser

from .exprs import (
    AddSubExpression,
    ColumnExpression,
    DivMulExpression,
    FunctionExpression,
    MeasureExpression,
)

# MAke a parser class with a pointer index


def to_ast(parser: Parser) -> Expression | None:
    """
    Convert a list of tokens into an abstract syntax tree (AST)
    """
    while parser:
        if ret := AddSubExpression.match(parser):
            return ret
        exit()
        if ret := DivMulExpression.match(parser):
            return ret
        if ret := ColumnExpression.match(parser):
            return ret
        if ret := FunctionExpression.match(parser):
            return ret
        if ret := MeasureExpression.match(parser):
            return ret
        else:
            raise ValueError(f"Unexpected token sequence: {parser[:3]}")
