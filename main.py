import json
from parser.parser import Parser
from parser.tokens import TokenType

from scanner import Scanner

statements = json.load(open("dax.json"))

for statement in statements:
    print(statement)
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
