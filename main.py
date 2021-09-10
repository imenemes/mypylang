from execute import *
from mylexer import MyLexer
from mypy_errors import Error,ParseError


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    while True:
        try:
            text = input('mypy> ')
        except EOFError:
            break
        if text:
            try:
                tree = parser.parse(lexer.tokenize(text))
                print(tree)
            except TypeError as err:
                raise ParseError(repr(err))
            try:
                Execute(tree, env)
            except TypeError as err:
                raise Error(repr(err))

    """text='si a == 2 alors a= 2*a sinon a= 5'
    tree= parser.parse(lexer.tokenize(text))
    print(tree)
    Execute(tree, env)"""