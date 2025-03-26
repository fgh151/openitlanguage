from sly import Lexer

class OpnitLexer(Lexer):
    tokens = {
        NUMBER, STRING,
        PLUS, MINUS, TIMES, DIVIDE,
        LPAREN, RPAREN, COMMA,
        ID,
        TRUE, FALSE,
        NEWLINE,
        FUNCTION, RETURN, VAR,
        LBRACE, RBRACE,
        COLON,
        SEMI,
        ARROW,  # Added for function return type
        TYPE,   # Added for type annotations
        ASSIGN  # Added for variable assignment
    }

    # Ignored characters
    ignore = ' \t'

    # Tokens
    ARROW = r'->'  # Must come before MINUS
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    LBRACE = r'\{'
    RBRACE = r'\}'
    COLON = r':'
    SEMI = r';'
    ASSIGN = r'='
    NEWLINE = r'\n+'

    # Keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['function'] = FUNCTION
    ID['return'] = RETURN
    ID['var'] = VAR
    ID['number'] = TYPE
    ID['string'] = TYPE
    ID['boolean'] = TYPE
    ID['any'] = TYPE

    # Special handling for comments
    @_(r'\#.*')
    def COMMENT(self, t):
        pass

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    # Line number tracking
    def __init__(self):
        super().__init__()
        self.lineno = 1

    def process_newline(self, t):
        self.lineno += t.value.count('\n') 