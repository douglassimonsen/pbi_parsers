import json

from parser.dax import Parser, Scanner, TokenType

x = "1"
statements = json.load(open("dax.json", encoding="utf-8"))

for j, statement in enumerate(statements):
    #     statement = """

    # """
    print(j, len(statements), statement)
    tokens = Scanner(statement).scan()
    tokens = list(
        filter(
            lambda x: x.tok_type
            not in {
                TokenType.WHITESPACE,
                TokenType.SINGLE_LINE_COMMENT,
                TokenType.MULTI_LINE_COMMENT,
            },
            tokens,
        ),
    )
    # for i, token in enumerate(tokens):
    #     print(i, token)
    p = Parser(tokens)
    a = p.to_ast()
    # print(a)
