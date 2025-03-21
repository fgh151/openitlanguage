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

    @_('statements')
    def program(self, p):
        return ('program', [s for s in p.statements if s is not None])

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('expr NEWLINE')
    def statement(self, p):
        return ('statement', p.expr)

    @_('NEWLINE')
    def statement(self, p):
        return None

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
        return ('funcall', p.ID, p.expr)

    @_('ID LPAREN expr COMMA expr RPAREN')
    def expr(self, p):
        return ('funcall2', p.ID, p.expr0, p.expr1)

    def error(self, token):
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                print(f'sly: Syntax error at line {lineno}, token={token.type}')
            else:
                print(f'sly: Syntax error, token={token.type}') 