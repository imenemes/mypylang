from mylexer import MyLexer
from myparser import MyParser
from execute import *
lexer = MyLexer()
parser = MyParser()
env={}
progs = [
#...
"5+4",
"4*2",
"8-2",
"6/2",
'scrap https://www.python.org/ "p"',
'fonc prg(): ecris "bonjour" #khjhgjfkhgkj*/;',

"prg()"


]
for i, prgm in enumerate(progs):
    print('TEST N. {}'.format(i))
    arbre = parser.parse(lexer.tokenize(prgm))
    try:
        #print(arbre)
        Execute(arbre, env)
    except Exception as err:
        print(repr(err))
        continue
