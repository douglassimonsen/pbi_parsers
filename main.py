import json
from parser.parser import Parser
from parser.tokens import TokenType

from parser.scanner import Scanner

statements = json.load(open("dax.json"))

for j, statement in enumerate(statements):
    statement = "VAR x = 1"
    print(j, statement)
    tokens = Scanner(statement).scan()
    tokens = list(filter(lambda x: x.type != TokenType.WHITESPACE, tokens))
    for i, token in enumerate(tokens):
        print(i, token)
    p = Parser(tokens)
    a = p.to_ast()
    if a is not None:
        print(a.pprint())
    print("""\n----""")
try:
    print(1)
except TypeError:
    pass
