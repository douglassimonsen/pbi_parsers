from pbi_parsers.dax import highlight_section, to_ast

input_dax = """
func.name(
    arg1 + 
      1 +
        2 + 3,
    func(),
    func(10000000000000),
    arg2
)
"""
ast = to_ast(input_dax)
assert ast is not None, "AST should not be None"
section = ast.args[0].right
highlighted = highlight_section(section)
print(highlighted.to_console())
