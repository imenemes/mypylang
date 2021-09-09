from execute import *


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    """while True:
        try:
            text = input('mypy> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
            Execute(tree, env)"""
    text='scrap https://www.python.org/ "p"'
    tree= parser.parse(lexer.tokenize(text))
    print(tree)
    Execute(tree, env)