import json
from parser.parser import Parser
from parser.scanner import Scanner
from parser.tokens import TokenType

statements = json.load(open("dax.json"))

for j, statement in enumerate(statements):
    statement = """
VAR counts =
IF(MAX(Appliance[Category]) = "Home Office",
    CALCULATE(COUNT('Home Office'[Appliance Title]), FILTER('Home Office', 'Home Office'[Appliance Title] = MAX(Appliance[Appliance Title]))),
IF(MAX(Appliance[Category]) = "Home Entertainment",
    CALCULATE(COUNT('Home Entertainment'[Appliance Title]), FILTER('Home Entertainment', 'Home Entertainment'[Appliance Title] = MAX(Appliance[Appliance Title]))),
IF(MAX(Appliance[Category]) = "Kitchen",
    CALCULATE(COUNT(Kitchen[Appliance Title]), FILTER('Kitchen', 'Kitchen'[Appliance Title] = MAX(Appliance[Appliance Title]))),
IF(MAX(Appliance[Category]) = "Bathroom",
    CALCULATE(COUNT(Bathroom[Appliance Title]), FILTER('Bathroom', 'Bathroom'[Appliance Title] = MAX(Appliance[Appliance Title]))),
IF(MAX(Appliance[Category]) = "Other Miscellaneous",
    CALCULATE(COUNT(Misc[Appliance Title]), FILTER('Misc', 'Misc'[Appliance Title] = MAX(Appliance[Appliance Title]))))))))
"""
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
    exit()
try:
    print(1)
except TypeError:
    pass
