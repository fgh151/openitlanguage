from sly import Parser
from .lexer import OpnitLexer

class OpnitParser(Parser):
    tokens = OpnitLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )

    def __init__(self):
        self.env = {}
        self.functions = {}

    @_('statements')
    def program(self, p):
        return ('program', [s for s in p.statements if s is not None])

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('function_def')
    def statement(self, p):
        return p.function_def

    @_('expr SEMI')
    def statement(self, p):
        return ('statement', p.expr)

    @_('expr NEWLINE')
    def statement(self, p):
        return ('statement', p.expr)

    @_('NEWLINE')
    def statement(self, p):
        return None

    @_('FUNCTION ID LPAREN param_list RPAREN ARROW type LBRACE statements RBRACE')
    def function_def(self, p):
        return ('function', p.ID, p.param_list, p.type, p.statements)

    @_('FUNCTION ID LPAREN RPAREN ARROW type LBRACE statements RBRACE')
    def function_def(self, p):
        return ('function', p.ID, [], p.type, p.statements)

    @_('param')
    def param_list(self, p):
        return [p.param]

    @_('param_list COMMA param')
    def param_list(self, p):
        return p.param_list + [p.param]

    @_('ID COLON type')
    def param(self, p):
        return (p.ID, p.type)

    @_('ID')
    def type(self, p):
        return p.ID

    @_('RETURN expr SEMI')
    def statement(self, p):
        return ('return', p.expr)

    @_('RETURN expr NEWLINE')
    def statement(self, p):
        return ('return', p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

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
        return ('funcall', p.ID, [p.expr])

    @_('ID LPAREN expr COMMA expr RPAREN')
    def expr(self, p):
        return ('funcall', p.ID, [p.expr0, p.expr1])

    @_('ID LPAREN expr COMMA expr COMMA expr RPAREN')
    def expr(self, p):
        return ('funcall', p.ID, [p.expr0, p.expr1, p.expr2])

    @_('ID LPAREN RPAREN')
    def expr(self, p):
        return ('funcall', p.ID, [])

    @_('ID')
    def expr(self, p):
        return ('var', p.ID)

    def error(self, token):
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                print(f'sly: Syntax error at line {lineno}, token={token.type}')
            else:
                print(f'sly: Syntax error, token={token.type}') 