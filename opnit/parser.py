from sly import Parser
from .lexer import OpnitLexer

class OpnitParser(Parser):
    tokens = OpnitLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', LBRACKET, RBRACKET),
    )

    def __init__(self):
        self.env = {}
        self.functions = {}

    @_('statements')
    def program(self, p):
        return ('program', [s for s in p.statements if s is not None])

    @_('statement')
    def statements(self, p):
        if p.statement is None:
            return []
        return [p.statement]

    @_('statements statement')
    def statements(self, p):
        if p.statement is None:
            return p.statements
        return p.statements + [p.statement]

    @_('function_def')
    def statement(self, p):
        return p.function_def

    @_('expr SEMI')
    def statement(self, p):
        return ('statement', p.expr)

    @_('NEWLINE')
    def statement(self, p):
        return None

    @_('WHILE LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('while', p.expr, p.statements)

    @_('FUNCTION ID LPAREN param_list RPAREN COLON TYPE LBRACE statements RBRACE')
    def function_def(self, p):
        return ('function', p.ID, p.param_list, p.TYPE, p.statements)

    @_('FUNCTION ID LPAREN RPAREN COLON TYPE LBRACE statements RBRACE')
    def function_def(self, p):
        return ('function', p.ID, [], p.TYPE, p.statements)

    @_('param')
    def param_list(self, p):
        return [p.param]

    @_('param_list COMMA param')
    def param_list(self, p):
        return p.param_list + [p.param]

    @_('ID COLON TYPE LBRACKET RBRACKET')
    def param(self, p):
        return (p.ID, f"{p.TYPE}[]")

    @_('ID COLON TYPE')
    def param(self, p):
        return (p.ID, p.TYPE)

    @_('RETURN expr SEMI')
    def statement(self, p):
        return ('return', p.expr)

    @_('VAR ID ASSIGN expr SEMI')
    def statement(self, p):
        return ('statement', ('assignment', p.ID, p.expr))

    @_('LBRACKET expr_list RBRACKET')
    def expr(self, p):
        return ('array_literal', p.expr_list)

    @_('LBRACKET RBRACKET')
    def expr(self, p):
        return ('array_literal', [])

    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('expr_list COMMA expr')
    def expr_list(self, p):
        return p.expr_list + [p.expr]

    @_('expr LBRACKET expr RBRACKET')
    def expr(self, p):
        return ('array_access', p.expr0, p.expr1)

    @_('expr PLUS expr')
    def expr(self, p):
        return ('binary', '+', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ('binary', '-', p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ('binary', '*', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ('binary', '/', p.expr0, p.expr1)

    @_('NUMBER')
    def expr(self, p):
        return ('number', p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ('string', p.STRING)

    @_('TRUE')
    def expr(self, p):
        return ('boolean', True)

    @_('FALSE')
    def expr(self, p):
        return ('boolean', False)

    @_('ID LPAREN expr RPAREN')
    def expr(self, p):
        return ('call', p.ID, [p.expr])

    @_('ID LPAREN expr COMMA expr RPAREN')
    def expr(self, p):
        return ('call', p.ID, [p.expr0, p.expr1])

    @_('ID LPAREN RPAREN')
    def expr(self, p):
        return ('call', p.ID, [])

    @_('ID')
    def expr(self, p):
        return ('variable', p.ID)

    def error(self, token):
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                print(f'sly: Syntax error at line {lineno}, token={token.type}')
            else:
                print(f'sly: Syntax error, token={token.type}') 