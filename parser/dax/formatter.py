import string
import textwrap

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


class Formatter:
    def __init__(self, expression: "Expression"):
        self.expression = expression

    def format(self) -> str:
        return self.format_helper(self.expression)

    @classmethod
    def format_helper(cls, expr: Expression) -> str:
        match expr:
            case AddSubExpression():
                return cls.format_add_sub(expr)
            case AddSubUnaryExpression():
                return cls.format_add_sub_unary(expr)
            case ArrayExpression():
                return cls.format_array(expr)
            case ComparisonExpression():
                return cls.format_bool(expr)
            case ColumnExpression():
                return cls.format_column(expr)
            case ConcatenationExpression():
                return cls.format_concatenation(expr)
            case DivMulExpression():
                return cls.format_div_mul(expr)
            case ExponentExpression():
                return cls.format_exponent(expr)
            case FunctionExpression():
                return cls.format_function(expr)
            case HierarchyExpression():
                return cls.format_hierarchy(expr)
            case IdentifierExpression():
                return cls.format_identifier(expr)
            case InExpression():
                return cls.format_in(expr)
            case KeywordExpression():
                return cls.format_keyword(expr)
            case LiteralStringExpression():
                return cls.format_literal_string(expr)
            case LiteralNumberExpression():
                return cls.format_literal_number(expr)
            case LogicalExpression():
                return cls.format_logical(expr)
            case MeasureExpression():
                return cls.format_measure(expr)
            case NoneExpression():
                return ""
            case ParenthesesExpression():
                return cls.format_parens(expr)
            case ReturnExpression():
                return cls.format_return(expr)
            case TableExpression():
                return cls.format_table(expr)
            case VariableExpression():
                return cls.format_variable(expr)
            case _:
                print(type(expr))
                print(expr)
                exit()
                return ""

    @classmethod
    def format_add_sub(cls, expr: AddSubExpression) -> str:
        left = cls.format_helper(expr.left)
        right = cls.format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def format_add_sub_unary(cls, expr: AddSubUnaryExpression) -> str:
        return f"{expr.operator.text}{cls.format_helper(expr.number)}"

    @classmethod
    def format_array(cls, expr: ArrayExpression) -> str:
        elements = ",\n".join(cls.format_helper(el) for el in expr.elements)
        elements = textwrap.indent(elements, " " * 4)[4:]
        return f"""{{
    {elements}
}}
"""

    @classmethod
    def format_comparison(cls, expr: ComparisonExpression) -> str:
        left = cls.format_helper(expr.left)
        right = cls.format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def format_column(cls, expr: ColumnExpression) -> str:
        table = expr.table.text
        if table.startswith("'") and all(
            c in string.ascii_letters + string.digits + "_" for c in table[1:-1]
        ):
            table = table[1:-1]
        column = expr.column.text
        return f"{table}{column}"

    @classmethod
    def format_concatenation(cls, expr: ConcatenationExpression) -> str:
        left = cls.format_helper(expr.left)
        right = cls.format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def format_div_mul(cls, expr: DivMulExpression) -> str:
        left = cls.format_helper(expr.left)
        right = cls.format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def format_exponent(cls, expr: ExponentExpression) -> str:
        base = cls.format_helper(expr.base)
        power = cls.format_helper(expr.power)
        return f"""{base}^{power}"""

    @classmethod
    def format_function(cls, expr: FunctionExpression) -> str:
        name = "".join(token.text for token in expr.name_parts)
        args = [cls.format_helper(arg) for arg in expr.args]
        if sum(len(x) for x in args) < 40:
            arg_str = ", ".join(args)
            return f"{name}({arg_str})"
        else:
            arg_str = textwrap.indent(",\n".join(args), " " * 4)[4:]
            return f"""
{name}(
    {arg_str}
)""".strip()

    @classmethod
    def format_hierarchy(cls, expr: HierarchyExpression) -> str:
        table = expr.table.text
        if table.startswith("'") and all(
            c in string.ascii_letters + string.digits + "_" for c in table[1:-1]
        ):
            table = table[1:-1]
        return f"{table}{expr.column.text}.{expr.level.text}"

    @classmethod
    def format_identifier(cls, expr: IdentifierExpression) -> str:
        return expr.name.text

    @classmethod
    def format_in(cls, expr: InExpression) -> str:
        value = cls.format_helper(expr.value)
        array = cls.format_helper(expr.array)
        return f"""{value} IN {array}"""

    @classmethod
    def format_keyword(cls, expr: KeywordExpression) -> str:
        return expr.name.text

    @classmethod
    def format_literal_string(cls, expr: LiteralStringExpression) -> str:
        return expr.value.text

    @classmethod
    def format_literal_number(cls, expr: LiteralNumberExpression) -> str:
        return expr.value.text

    @classmethod
    def format_logical(cls, expr: LogicalExpression) -> str:
        left = cls.format_helper(expr.left)
        right = cls.format_helper(expr.right)
        return f"""{left} {expr.operator.text} {right}"""

    @classmethod
    def format_measure(cls, expr: MeasureExpression) -> str:
        return expr.name.text

    @classmethod
    def format_parens(cls, expr: ParenthesesExpression) -> str:
        inner = cls.format_helper(expr.inner_statement)
        return f"({inner})"

    @classmethod
    def format_return(cls, expr: ReturnExpression) -> str:
        variable_strs = "\n".join(
            cls.format_helper(var) for var in expr.variable_statements
        )
        return_statement: str = cls.format_helper(expr.ret)
        return f"""
{variable_strs}        
RETURN {return_statement}
""".strip()

    @classmethod
    def format_table(cls, expr: TableExpression) -> str:
        table_name = expr.name.text
        if table_name.startswith("'") and all(
            c in string.ascii_letters + string.digits + "_" for c in table_name[1:-1]
        ):
            table_name = table_name[1:-1]
        return table_name

    @classmethod
    def format_variable(cls, expr: VariableExpression) -> str:
        return f"{expr.var_name.text} = {cls.format_helper(expr.statement)}"
