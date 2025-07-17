from pbi_parsers.dax.lexer import Lexer

x = Lexer("12.3e10").scan()
print(x)
