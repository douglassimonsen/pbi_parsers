# Overview

Based on [Crafting Interpreters](https://timothya.com/pdfs/crafting-interpreters.pdf). Library provides lexers, parsers, and formatters for DAX and Power Query (M) languages. Designed to support code introspection and analysis, not execution. This enables development of [ruff](https://github.com/astral-sh/ruff)-equivalent tools for DAX and Power Query. It also enables extracting metadata from DAX and Power Query code, such PQ source types (Excel, SQL, etc.) and DAX lineage dependencies.

# Installation

```shell
python -m pip install pbi_parsers
```

## Functionality

!!! info "Rust Implementation"
    Although the library is primarily implemented in Python, there are plans to implement a Rust version for performance and additional type-safety.

- DAX
    * [x] Lexer
    * [x] Parser
    * [x] Formatter
    * [x] Testing
    * [ ] Rust Implementation
- Power Query (M)
    * [x] Lexer
    * [x] Parser
    * [ ] Formatter
    * [ ] Testing
    * [ ] Rust Implementation
  

## Examples

!!! info "Formatting DAX Expressions"
    Like `ruff` for Python, this library can format DAX expressions to improve readability and maintainability.

    ```python
    from pbi_parsers.dax import format_expression

    input_dax = """
    func.name(arg1 + 1 + 2  + 3, func(), func(10000000000000), arg2)
    """
    formatted_dax = format_expression(input_dax)
    print(formatted_dax)
    # Output:
    # func.name(
    #     arg1 + 1 + 2 + 3,
    #     func(),
    #     func(10000000000000),
    #     arg2
    # )
    ```

!!! info "Creating AST Trees from DAX Expressions"
    The library can parse DAX expressions into Abstract Syntax Trees (ASTs) for further analysis or manipulation.

    ```python
    from pbi_parsers.dax import to_ast

    input_dax = """
    func.name(arg1 + 1 + 2  + 3, func(), func(10000000000000), arg2)
    """
    ast = to_ast(input_dax)
    print(ast)
    # Output: 
    # Function (
    #     name: func.name,
    #     args: Add (
    #               left: Identifier (arg1),
    #               right: Add (
    #                          left: Number (1),
    #                          right: Add (
    #                                     left: Number (2),
    #                                     right: Number (3)
    #                                 )
    #                      )
    #           ),
    #           Function (
    #               name: func,
    #               args:
    #           ),
    #           Function (
    #               name: func,
    #               args: Number (10000000000000)
    #           ),
    #           Identifier (arg2)
    # )
    ```

!!! info "Highlighting DAX Sections"
    The library can highlight sections of DAX code, making it easier to identify and analyze specific parts of the code.

    Note: in the console, the caret (`^`) will be yellow and the line number will be cyan.

    ```python
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
    section = ast.args[0].right.left  # the "1" in "arg1 + 1 + 2 + 3"
    highlighted = highlight_section(section)
    print(highlighted.to_console())

    # Output:
    # 1 | func.name(
    # 2 |     arg1 +
    # 3 |       1 +
    #         ^
    # 4 |         2 + 3,
    # 5 |     func(),
    ```

    Highlighting a larger section:

    ```python
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
    section = ast.args[0].right # The "1 + 2" in "arg1 + 1 + 2 + 3"
    highlighted = highlight_section(section)
    print(highlighted.to_console())
    # Output:
    # 1 | func.name(
    # 2 |     arg1 +
    # 3 |       1 +
    #         ^^^
    # 4 |         2 + 3,
    # ^^^^^^^^^^^^^^^^^
    # 5 |     func(),
    # 6 |     func(10000000000000),

    ```