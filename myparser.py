from sly import Parser

from mylexer import *

class MyParser(Parser):
    tokens = MyLexer.tokens

    # traitement des priorités

    precedence = (
        ('left', 'DOUBLE', 'TYPE', 'CONCA','SCRAPE'),
        ('left', '+', '-'),
        ('left', '*', '/', '^','MOD'),
        ('right', 'UMINUS'),

    )

    # fonction d'initialisation
    def __init__(self):
        self.env = {}

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % str(t.value))
            # self.index += 1


    # fonction qui traite les espaces en les ignorant
    @_('')
    def statement(self, p):
        pass

    @_('POUR variable FLECHE expr ALORS statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.variable, p.expr), p.statement)

    @_('SI condition ALORS statement SINON statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FONC NOM "(" NOM ")" DEUP statement')
    def statement(self, p):
        return ('fun_def', p.NOM, p.statement)

    @_('SCRAPE URL CHAINE')
    def statement(self, p):
        return ('SCRP', p.URL, p.CHAINE)

    @_('NOM "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NOM)

    @_('variable')
    def statement(self, p):
        return p.variable

    @_('NOM "=" expr')
    def variable(self, p):
        return ('variable', p.NOM, p.expr)

    @_('NOM "=" CHAINE')
    def variable(self, p):
        return ('variable', p.NOM, p.CHAINE)

    @_('TYPE CHAINE')
    def expr(self, p):
        return('tp',p.CHAINE)

    @_('TYPE expr')
    def expr(self, p):
        return ('tp',p.expr)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return ('paw', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr[1]

    @_('expr MOD  expr')
    def expr(self, p):
        return ('rst', p.expr0, p.expr1)

    @_('expr EGALE expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('ECRIS CHAINE')
    def expr(self, p):
        return ('ecr', p.CHAINE)

    @_('CONCA CHAINE CHAINE')
    def expr(self, p):
        return ('conca', p.CHAINE0, p.CHAINE1)

    @_('DOUBLE CHAINE')
    def expr(self, p):
        return ('dbl', p.CHAINE)

    @_('DOUBLE expr')
    def expr(self, p):
        return ('dbl', p.expr)

    @_('NOM')
    def expr(self, p):
        return ('var', p.NOM)

    @_('NUM')
    def expr(self, p):
        return ('num', p.NUM)

    @_('FLOAT')
    def expr(self, p):
        return ('flt', p.FLOAT)
