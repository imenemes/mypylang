from mylexer import MyLexer
from myparser import MyParser
from execute import Execute
from mypy_errors import Error,ParseError
lexer = MyLexer()
parser = MyParser()
env = {}
progs = [
#...
"5+4",#0
"4*2",#1
"8-2",#2
"6/2",#3
"ecris bb",#4
"""scrap https://weather.com/fr-FR/temps/10jours/l/1975528fb7e3553b7eacfe7ac89b421986bb9949c2506b144b4e228d57da124b "p" """,#5
'fonc prg(): ecris "test réussi" #khjhgjfkhgkj*/;',#6
'fonc prg2(B): ecris "sss" #khjhgjfkhgkj*/;',#7
"prg()",#8
"prg2(B)",#9
"a = 2",#10
"a",#11
"""si a == 2 alors b= 2*a 
sinon b= 5""",# 12
"b",# 13
"""
type "bjr"  
""",#14
"type a",#15
"pour a=2 -> 5 alors 2*a",#16
"""
conca "bon" "jouR"
""",#17
"5/0",#18
"a=2",
"si a < 2 alors b= 2*a sinon",
"b",
"double 3"



]
for i, prgm in enumerate(progs):
    print('TEST N. {}'.format(i))
    try:
        tree = parser.parse(lexer.tokenize(prgm))
    except (AttributeError,ZeroDivisionError) as err:
        print(repr(err))
        continue
    try:
        Execute(tree, env)
    except ZeroDivisionError as err:
         print(repr(err))
         continue
    except:
        print("Unexpected error %s", tree)
        continue


