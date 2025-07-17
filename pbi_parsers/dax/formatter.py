import string
import textwrap
from typing import Any

from .exprs import (
    AddSubExpression,
    AddSubUnaryExpression,
    ArrayExpression,
    ColumnExpression,
    ComparisonExpression,
    ConcatenationExpression,
    DivMulExpression,
    ExponentExpression,
    Expression,
    FunctionExpression,
    HierarchyExpression,
    IdentifierExpression,
    InExpression,
    KeywordExpression,
    LiteralNumberExpression,
    LiteralStringExpression,
    LogicalExpression,
    MeasureExpression,
    NoneExpression,
    ParenthesesExpression,
    ReturnExpression,
    TableExpression,
    VariableExpression,
)

MAX_ARGUMENT_LENGTH = 40  # Maximum length of arguments before formatting them on new lines


class Formatter:
    """Formats a DAX expression into a standardized format."""

    def __init__(self, expression: "Expression") -> None:
        self.expression = expression

    def format(self) -> str:
        return self._format_helper(self.expression)

    @classmethod
    def _format_helper(cls, expr: Expression) -> str:
        mapper: Any = {
            AddSubExpression: cls._format_add_sub,
            AddSubUnaryExpression: cls._format_add_sub_unary,
            ArrayExpression: cls._format_array,
            ComparisonExpression: cls._format_comparison,
            ColumnExpression: cls._format_column,
            ConcatenationExpression: cls._format_concatenation,
            DivMulExpression: cls._format_div_mul,
            ExponentExpression: cls._format_exponent,
            FunctionExpression: cls._format_function,
            HierarchyExpression: cls._format_hierarchy,
            IdentifierExpression: cls._format_identifier,
            InExpression: cls._format_in,
            KeywordExpression: cls._format_keyword,
            LiteralNumberExpression: cls._format_literal_number,
            LiteralStringExpression: cls._format_literal_string,
            LogicalExpression: cls._format_logical,
            MeasureExpression: cls._format_measure,
            NoneExpression: lambda _: "",
            ParenthesesExpression: cls._format_parens,
            ReturnExpression: cls._format_return,
            TableExpression: cls._format_table,
            VariableExpression: cls._format_variable,
        }
        if type(expr) in mapper:
            return mapper[type(expr)](expr)
        msg = f"Unsupported expression type: {type(expr).__name__}"
        raise TypeError(msg)

    @classmethod
    def _format_add_sub(cls, expr: AddSubExpression) -> str:
        left = cls._format_helper(expr.left)
        right = cls._format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def _format_add_sub_unary(cls, expr: AddSubUnaryExpression) -> str:
        return f"{expr.operator.text}{cls._format_helper(expr.number)}"

    @classmethod
    def _format_array(cls, expr: ArrayExpression) -> str:
        elements = ",\n".join(cls._format_helper(el) for el in expr.elements)
        elements = textwrap.indent(elements, " " * 4)[4:]
        return f"""{{
    {elements}
}}
"""

    @classmethod
    def _format_comparison(cls, expr: ComparisonExpression) -> str:
        left = cls._format_helper(expr.left)
        right = cls._format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def _format_column(cls, expr: ColumnExpression) -> str:
        table = expr.table.text
        if table.startswith("'") and all(c in string.ascii_letters + string.digits + "_" for c in table[1:-1]):
            table = table[1:-1]
        column = expr.column.text
        return f"{table}{column}"

    @classmethod
    def _format_concatenation(cls, expr: ConcatenationExpression) -> str:
        left = cls._format_helper(expr.left)
        right = cls._format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def _format_div_mul(cls, expr: DivMulExpression) -> str:
        left = cls._format_helper(expr.left)
        right = cls._format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def _format_exponent(cls, expr: ExponentExpression) -> str:
        base = cls._format_helper(expr.base)
        power = cls._format_helper(expr.power)
        return f"""{base}^{power}"""

    @classmethod
    def _format_function(cls, expr: FunctionExpression) -> str:
        name = "".join(token.text for token in expr.name_parts)
        args = [cls._format_helper(arg) for arg in expr.args]
        if sum(len(x) for x in args) < MAX_ARGUMENT_LENGTH:
            arg_str = ", ".join(args)
            return f"{name}({arg_str})"
        arg_str = textwrap.indent(",\n".join(args), " " * 4)[4:]
        return f"""
{name}(
    {arg_str}
)""".strip()

    @classmethod
    def _format_hierarchy(cls, expr: HierarchyExpression) -> str:
        table = expr.table.text
        if table.startswith("'") and all(c in string.ascii_letters + string.digits + "_" for c in table[1:-1]):
            table = table[1:-1]
        return f"{table}{expr.column.text}.{expr.level.text}"

    @classmethod
    def _format_identifier(cls, expr: IdentifierExpression) -> str:
        return expr.name.text

    @classmethod
    def _format_in(cls, expr: InExpression) -> str:
        value = cls._format_helper(expr.value)
        array = cls._format_helper(expr.array)
        return f"""{value} IN {array}"""

    @classmethod
    def _format_keyword(cls, expr: KeywordExpression) -> str:
        return expr.name.text

    @classmethod
    def _format_literal_string(cls, expr: LiteralStringExpression) -> str:
        return expr.value.text

    @classmethod
    def _format_literal_number(cls, expr: LiteralNumberExpression) -> str:
        return expr.value.text

    @classmethod
    def _format_logical(cls, expr: LogicalExpression) -> str:
        left = cls._format_helper(expr.left)
        right = cls._format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def _format_measure(cls, expr: MeasureExpression) -> str:
        return expr.name.text

    @classmethod
    def _format_parens(cls, expr: ParenthesesExpression) -> str:
        inner = cls._format_helper(expr.inner_statement)
        return f"({inner})"

    @classmethod
    def _format_return(cls, expr: ReturnExpression) -> str:
        variable_strs = "\n".join(cls._format_helper(var) for var in expr.variable_statements)
        return_statement: str = cls._format_helper(expr.ret)
        return f"""
{variable_strs}
RETURN {return_statement}
""".strip()

    @classmethod
    def _format_table(cls, expr: TableExpression) -> str:
        table_name = expr.name.text
        if table_name.startswith("'") and all(
            c in string.ascii_letters + string.digits + "_" for c in table_name[1:-1]
        ):
            table_name = table_name[1:-1]
        return table_name

    @classmethod
    def _format_variable(cls, expr: VariableExpression) -> str:
        return f"{expr.var_name.text} = {cls._format_helper(expr.statement)}"
