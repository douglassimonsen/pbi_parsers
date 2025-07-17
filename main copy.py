import json
from parser.pq import Scanner

statements = json.load(open("pqs.json"))

for j, statement in enumerate(statements):
    if statement.lower().startswith("calendar"):
        continue
    # print(statement)
    tokens = Scanner(statement).scan()
    print(tokens)
    exit()
    # tokens = list(
    #     filter(
    #         lambda x: x.type
    #         not in (
    #             TokenType.WHITESPACE,
    #             TokenType.SINGLE_LINE_COMMENT,
    #             TokenType.MULTI_LINE_COMMENT,
    #         ),
    #         tokens,
    #     )
    # )
    # for i, token in enumerate(tokens):
    #     print(i, token)
    # p = Parser(tokens)
    # a = p.to_ast()
    # if a is not None:
    #     print(a.pprint())
