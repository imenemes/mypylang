****************************************
# Nom ......... : mypy.py
# Rôle ........ : calculette simple en SLY python avec quelques commandes en français
# Auteur ...... : Imen L'Hocine
# Version ..... : V0.1 du 19/02/2021
# Licence ..... : réalisé dans le cadre du cours de C&I L3/chapitre 5
# (../..)
# Pour exécuter : python3 mypy.py
# Usage :  : vous aurez un prompt mypy>  vous pourrez faire des opérations arithmtiques et quelques commandes en français
# ********************************************************


from sly import Lexer
from sly import Parser


class Lexer(Lexer):
    tokens = {NOM, NUM, CHAINE, ECRIS, CONCA, DOUBLE, MOD}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*'}

    # Define tokens

    MOD = r'MOD'
    DOUBLE = r'DOUBLE'
    CONCA = r'CONCA'
    ECRIS = r'ECRIS'
    NOM = r'[a-zA-Z_][a-zA-Z0-9_]*'
    CHAINE = r'\".*?\"'

    # fonction qui detecte un nombre et retourne sa valeur
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # fonction qui qui traite les sauts de ligne
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


class Parser(Parser):
    tokens = Lexer.tokens

    # traitement des priorité

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        ('left', 'DOUBLE', 'MOD'),
    )

    # fonction d'initialisation
    def __init__(self):
        self.env = {}

    # fonction qui traite les espaces en les ignorant
    @_('')
    def statement(self, p):
        pass

    @_('variable')
    def statement(self, p):
        return p.variable

    @_('NOM "=" expr')
    def variable(self, p):
        return ('variable', p.NOM, p.expr)

    @_('NOM "=" CHAINE')
    def variable(self, p):
        return ('variable', p.NOM, p.CHAINE)

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

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NOM')
    def expr(self, p):
        return ('var', p.NOM)

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

    @_('expr MOD  expr')
    def expr(self, p):
        return ('rst', p.expr0, p.expr1)

    @_('NUM')
    def expr(self, p):
        return ('num', p.NUM)


class Execute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'rst':
            return self.walkTree(node[1]) % self.walkTree(node[2])
        elif node[0] == 'ecr':
            return self.walkTree(node[1])
        elif node[0] == 'conca':
            return (self.walkTree(node[1]))[:-1] + (self.walkTree(node[2]))[1:]

        elif node[0] == 'dbl':
            if (node[1][0] == 'num'):
                return 2 * self.walkTree(node[1])
            else:
                return (self.walkTree(node[1]))[:-1] + (self.walkTree(node[1]))[1:]

        elif node[0] == 'variable':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        elif node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable indéfinie '" + node[1] + "'")
                return 0


if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()
    env = {}
    while True:
        try:
            text = input('mypy > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            Execute(tree, env)
