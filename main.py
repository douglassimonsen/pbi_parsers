import json
from parser.parser import Parser
from parser.tokens import TokenType
from pprint import pprint

from scanner import Scanner

statements = json.load(open("dax.json"))

for statement in statements:
    statement = "1 + 3 / 1"  # asd
    print(statement)
    tokens = Scanner(statement).scan()
    tokens = list(filter(lambda x: x.type != TokenType.WHITESPACE, tokens))
    for token in tokens:
        pprint(token)
    p = Parser(tokens)
    a = p.to_ast()
    if a is not None:
        print(a.pprint())
    print("""\n----""")
    exit()
try:
    print(1)
except TypeError:
    pass
