import json

from expressions import to_ast
from scanner import Scanner
from tokens import TokenType

statements = json.load(open("dax.json"))

for statement in statements:
    print(statement)
    tokens = Scanner(statement).scan()
    tokens = [token for token in tokens if token.type != TokenType.WHITESPACE]
    for token in tokens:
        print(token)
    print(to_ast(tokens).pprint())
    print("----")
