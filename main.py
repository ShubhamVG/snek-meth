from meth import Interpreter
from lexer import Lexer
from parser import Parser
from utils import Num

if __name__ == '__main__':
    while True:
        expr = input('Expr: ')
        x = input('x: ')
        y = input('y: ')
        var_dict: dict[str, Num] = {}

        try:
            val = Num(x)
            var_dict['x'] = val
            val = Num(y)
            var_dict['y'] = val
        except:
            pass

        print(var_dict)

        lex = Lexer(expr)
        tokens = lex.get_tokens()
        print(tokens)
        par = Parser(tokens)
        ast = par.get_syntax_tree()
        print(ast)
        engine = Interpreter(ast)
        print(engine.evaluate(var_dict))
