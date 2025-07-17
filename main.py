import json
from parser.parser import Parser
from parser.scanner import Scanner
from parser.tokens import TokenType

statements = json.load(open("dax.json"))

for j, statement in enumerate(statements):
    print(statement)
    tokens = Scanner(statement).scan()
    tokens = list(
        filter(
            lambda x: x.type
            not in (
                TokenType.WHITESPACE,
                TokenType.SINGLE_LINE_COMMENT,
                TokenType.MULTI_LINE_COMMENT,
            ),
            tokens,
        )
    )
    for i, token in enumerate(tokens):
        print(i, token)
    p = Parser(tokens)
    a = p.to_ast()
    if a is not None:
        print(a.pprint())
    breakpoint()
    print("""\n----""")
