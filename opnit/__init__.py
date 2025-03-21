from .lexer import OpnitLexer
from .parser import OpnitParser
from .interpreter import OpnitInterpreter

def run(code):
    lexer = OpnitLexer()
    parser = OpnitParser()
    interpreter = OpnitInterpreter()
    
    tokens = lexer.tokenize(code)
    tree = parser.parse(tokens)
    return interpreter.evaluate(tree) 