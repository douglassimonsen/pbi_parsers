import json
from parser.pq import Parser, Scanner, TokenType

statements = json.load(open("pqs.json"))

for j, statement in enumerate(statements):
    statement = """
 let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("--bin--", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [Date = _t])
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Date", type date}}),
    #"Inserted Month Name" = Table.AddColumn(#"Changed Type", "Month Name", each Date.MonthName([Date]), type text),
    #"Extracted First Characters" = Table.TransformColumns(#"Inserted Month Name", {{"Month Name", each Text.Start(_, 3), type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Extracted First Characters",{{"Month Name", "Month"}}),     
    #"Inserted Year" = Table.AddColumn(#"Renamed Columns", "Year", each Date.Year([Date]), Int64.Type),    
    #"Changed Type1" = Table.TransformColumnTypes(#"Inserted Year",{{"Year", type text}}),
    #"Inserted Month" = Table.AddColumn(#"Changed Type1", "Month.1", each Date.Month([Date]), Int64.Type), 
    #"Renamed Columns1" = Table.RenameColumns(#"Inserted Month",{{"Month.1", "MonthN"}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns1",{"Date", "Month", "MonthN", "Year"})   
in
    #"Reordered Columns"
"""
    statement = """
 ((type text) meta [Serialized.Text = true])
"""
    print(j, len(statements), statement)
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
    exit()
