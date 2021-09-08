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
        result = self.walkTree(tree)

        # cas du résultat numérique
        if result is not None and (isinstance(result, int) or isinstance(result, float)):
            print(result)
        # cas d'un chaine
        if isinstance(result, str) and result[0] == '"':
            print(result)

    # methode walktree qui constitue l'arbre
    def walkTree(self, node):

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

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])
        #rajouter > et < (pour éviter les redondances je pense à un dictionnaire)
        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'SCRP':
            try:
                html = urlopen(self.walkTree(node[1]))
            except Exception as e:
                print(str(e))
            else:
                res = BeautifulSoup(html.read(), "lxml")
                tag = 'res.%s.getText()' %self.walkTree(node[2])[1:-1]
                if tag is None :
                    print("Tag not found")
                else:
                    print(eval(tag))

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


        elif node[0] == 'paw':
            return self.walkTree(node[1]) ** self.walkTree(node[2])

        elif node[0] == 'dbl':
            if (node[1][0] == 'num'or node[1][0] == 'flt' ):
                return 2 * self.walkTree(node[1])
            else:
                return (self.walkTree(node[1]))[:-1] + (self.walkTree(node[1]))[1:]

        elif node[0] == 'variable':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        elif node[0] == 'tp':
            print(node[1])
            print(type(self.walkTree(node[1])))

        elif node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable indéfinie '" + node[1] + "'")
                return 0

        elif node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        elif node[0] == 'for_loop_setup':
            return self.walkTree(node[1]), self.walkTree(node[2])

        #else: print("Ce type n'est pas pris en charge par ce langage ")




