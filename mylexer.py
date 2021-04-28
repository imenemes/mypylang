from sly import Lexer


class MyLexer(Lexer):
    tokens = {NOM, NUM, CHAINE, ECRIS, CONCA, DOUBLE, MOD,FLOAT,TYPE,SI,ALORS, SINON,EGALE, FONC,DEUP,POUR,FLECHE, SCRAPE , URL}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*','^','(',')','//'}

    # Define tokens

    MOD = r'MOD'
    SINON = r'SINON'
    SI = r'SI'
    FONC = r'FONC'
    POUR = r'POUR'
    ALORS = r'ALORS'
    DOUBLE = r'DOUBLE'
    CONCA = r'CONCA'
    ECRIS = r'ECRIS'
    TYPE = r'TYPE'
    DEUP = r':'
    EGALE = r'=='
    FLECHE = r'->'
    CHAINE = r'\".*?\"'
    SCRAPE = r'SCRAPE'
    URL = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}'
    NOM = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # fonction qui detecte un nombre et retourne sa valeur
    @_(r'([0-9]*\.[1-9]+)([Ee][+-]?[0-9]+)?')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t


    # fonction qui detecte un nombre et retourne sa valeur
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # fonction qui qui traite les sauts de ligne
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

    @_(r'//.*')
    def COMMENT(self, t):
        pass

