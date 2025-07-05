import json
from pathlib import Path

from pbi_parsers.pq import Parser, Scanner, TokenType

with Path("pqs.json").open(encoding="utf-8") as f:
    statements = json.load(f)

for j, statement in enumerate(statements):
    # statement = r"""
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
    for i, token in enumerate(tokens):
        print(i, token)
    p = Parser(tokens)
    a = p.to_ast()
    # exit()
