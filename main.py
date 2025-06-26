import json

from scanner import Scanner

statements = json.load(open("dax.json"))

for statement in statements:
    print(statement)
    Scanner(statement).scan()
    print("----")
