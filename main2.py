import json
from parser.pq import Parser, Scanner, TokenType

statements = json.load(open("pqs.json"))

for j, statement in enumerate(statements):
    print(statement)
    tokens = Scanner(statement).scan()
    tokens = list(
        filter(
            lambda x: x.type not in (TokenType.WHITESPACE,),
            tokens,
        )
    )
    for i, token in enumerate(tokens):
        print(i, token)
    p = Parser(tokens)
    a = p.to_ast()
    # if a is not None:
    #     print(a.pprint())
    exit()
