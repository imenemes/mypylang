#!/usr/bin/env python3

from mypy.execute import *
from mypy.mylexer import MyLexer


def main():
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    print('mypyfr 1.0 (default, sept 05 2022)\n' 
          'Tapez "help" pour plus d\'information sur le langage, "ex" pour des exemples d\'utilisation quit pour quitter.')
    while True:
        try:
            text = input('mypy> ')
        except EOFError:
            break
        if text:
            try:
                tree = parser.parse(lexer.tokenize(text))
            except(AttributeError) as err:
                print(repr(err))
                continue
            try:
                Execute(tree, env)
            except (ZeroDivisionError,IndexError) as err:
                print(repr(err))
                continue
            except:
                print("erreur innatendue")
                continue


if __name__ == "__main__":
    main()

