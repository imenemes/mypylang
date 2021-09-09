#****************************************
# Nom ......... : mypy.py
# Rôle ........ : langage avec commandes en français
# Auteur ...... : Imen L'Hocine
# Version ..... : V0.1 du 19/02/2021
# Licence ..... : réalisé dans le cadre du cours de C&I L3/chapitre 10
# (../..)
# Pour exécuter : python3 mypy.py
# Usage :  : vous aurez un prompt mypy>  vous pourrez faire des opérations arithmtiques et quelques commandes en français
# ********************************************************


from myparser import *
from urllib.request import *
from bs4 import BeautifulSoup

# la classe execute


class Execute:
    # methode init
    def __init__(self, tree, env):
        self.env = env
        result = self.traverse(tree)

        # cas du résultat numérique
        if result is not None and (isinstance(result, int) or isinstance(result, float)):
            print(result)
        # cas d'un chaine
        if isinstance(result, str) and result[0] == '"':
            print(result)

    # methode traverse qui traverse l'arbre syntaxique
    def traverse(self, node):

        if isinstance(node, float):
            return node
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'num':
            return node[1]

        if node[0] == 'flt':
            return node[1]

        if node[0] == 'str':
            return node[1]

        # traitements des opérateurs arithmétiques
        if node[0] == '+':
            return self.traverse(node[1]) + self.traverse(node[2])
        elif node[0] == '-':
            return self.traverse(node[1]) - self.traverse(node[2])
        elif node[0] == '*':
            return self.traverse(node[1]) * self.traverse(node[2])
        elif node[0] == '/':
            return self.traverse(node[1]) / self.traverse(node[2])
        elif node[0] == '%':
            return self.traverse(node[1]) % self.traverse(node[2])
        elif node[0] == '^':
            return self.traverse(node[1]) ** self.traverse(node[2])
        # traitementdes opérateurs de comparaisons litéraux
        elif node[0] == '>':
            return self.traverse(node[1]) ** self.traverse(node[2])
        elif node[0] == '<':
            return self.traverse(node[1]) ** self.traverse(node[2])
        if node[0] == 'PE':
            return self.traverse(node[1]) <= self.traverse(node[2])
        if node[0] == 'GE':
            return self.traverse(node[1]) >= self.traverse(node[2])
        if node[0] == 'NE':
            return self.traverse(node[1]) != self.traverse(node[2])
        if node[0] == 'EGL':
            return self.traverse(node[1]) == self.traverse(node[2])


        if node[0] == 'if_stmt':
            result = self.traverse(node[1])
            if result:
                return self.traverse(node[2][1])
            return self.traverse(node[2][2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.traverse(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'SCRP':
            try:
                html = urlopen(self.traverse(node[1]))
            except Exception as e:
                print(str(e))
            else:
                res = BeautifulSoup(html.read(), "lxml")
                tag = 'res.%s.getText()' %self.traverse(node[2])[1:-1]
                if tag is None :
                    print("Tag not found")
                else:
                    print(eval(tag))

        # traitement de l'opération echo
        elif node[0] == 'ecr':
            return self.traverse(node[1])
        # concaténation de deux chaines
        elif node[0] == 'conca':
            return (self.traverse(node[1]))[:-1] + (self.traverse(node[2]))[1:]

        elif node[0] == 'dbl':
            if (node[1][0] == 'num'or node[1][0] == 'flt' ):
                return 2 * self.traverse(node[1])
            else:
                return (self.traverse(node[1]))[:-1] + (self.traverse(node[1]))[1:]

        elif node[0] == 'variable':
            self.env[node[1]] = self.traverse(node[2])
            return node[1]

        elif node[0] == 'tp':
            print(node[1])
            print(type(self.traverse(node[1])))

        elif node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable indéfinie '" + node[1] + "'")
                return 0

        elif node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.traverse(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.traverse(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        elif node[0] == 'for_loop_setup':
            return self.traverse(node[1]), self.traverse(node[2])




