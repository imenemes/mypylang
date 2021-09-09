from sly import Parser

from mylexer import *


class MyParser(Parser):
    tokens = MyLexer.tokens

    # traitement des priorités

    precedence = (
        ('nonassoc', '<', 'PE', '>', 'GE','EGL', 'NE'),
        ('nonassoc', 'DOUBLE', 'TYPE', 'CONCA', 'SCRAPE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%','x'),
        ('right', '^'),
        ('right', 'UMINUS')

    )

    # fonction d'initialisation
    def __init__(self):
        self.env = {}

    # fonction qui traite les espaces en les ignorant
    @_('')
    def statement(self, p):
        pass

    @_('CHAINE')
    def statement(self, p):
        return 'str', p.CHAINE

    @_('POUR variable FLECHE expr ALORS statement')
    def statement(self, p):
        return 'for_loop', ('for_loop_setup', p.variable, p.expr), p.statement

    @_('SI condition ALORS statement SINON statement')
    def statement(self, p):
        return 'if_stmt', p.condition, ('branch', p.statement0, p.statement1)

    @_('FONC NOM "(" ")" ":" statement')
    def statement(self, p):
        return 'fun_def', p.NOM, p.statement

    @_('SCRAPE URL CHAINE')
    def statement(self, p):
        return 'SCRP', p.URL, p.CHAINE

    @_('NOM "(" ")"')
    def statement(self, p):
        return 'fun_call', p.NOM

    @_('variable')
    def statement(self, p):
        return p.variable

    @_('NOM "=" expr')
    def variable(self, p):
        return 'variable', p.NOM, p.expr

    @_('NOM "=" CHAINE')
    def variable(self, p):
        return 'variable', p.NOM, p.CHAINE

    @_('TYPE CHAINE')
    def expr(self, p):
        return 'tp', p.CHAINE

    @_('TYPE expr')
    def expr(self, p):
        return 'tp', p.expr

    @_('expr')
    def statement(self, p):
        return p.expr

    # construire l'arbre des opérateurs arithmétiques
    @_('expr "+" expr',
       'expr "-" expr',
       'expr "x" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr "^" expr',
       'expr "%" expr',
       'expr ">" expr',
       'expr "<" expr'
       )
    def expr(self, p):
        return p[1], p.expr0, p.expr1

    # traitement du '-' unaire
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr[1]

    @_('expr EGL expr',
       'expr PE expr',
       'expr GE expr',
       'expr NE expr')
    def condition(self, p):
        return p[1], p.expr0, p.expr1


    # d'autres opérations
    @_('ECRIS CHAINE')
    def expr(self, p):
        return 'ecr', p.CHAINE

    @_('CONCA CHAINE CHAINE')
    def expr(self, p):
        return 'conca', p.CHAINE0, p.CHAINE1

    @_('DOUBLE CHAINE')
    def expr(self, p):
        return 'dbl', p.CHAINE

    @_('DOUBLE expr')
    def expr(self, p):
        return 'dbl', p.expr

    @_('NOM')
    def expr(self, p):
        return 'var', p.NOM

    @_('NUM')
    def expr(self, p):
        return 'num', p.NUM

    @_('FLOAT')
    def expr(self, p):
        return 'flt', p.FLOAT

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr



if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    while True:
        try:
            text = input('YACC> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
