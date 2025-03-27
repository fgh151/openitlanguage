from sly import Lexer

class OpnitLexer(Lexer):
    tokens = {
        NUMBER, STRING,
        PLUS, MINUS, TIMES, DIVIDE,
        LPAREN, RPAREN, COMMA,
        LBRACKET, RBRACKET,  # Array brackets
        LBRACE, RBRACE,
        ID,
        TRUE, FALSE,
        NEWLINE,
        FUNCTION, RETURN, VAR,
        COLON,
        SEMI,
        TYPE,   # Added for type annotations
        ASSIGN,  # Added for variable assignment
        WHILE  # Add WHILE token
    }

    # Ignored characters
    ignore = ' \t'
    ignore_comment = r'//.*'  # Line comments

    # Tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COMMA = r','
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
    ID['while'] = WHILE
    ID['number'] = TYPE
    ID['string'] = TYPE
    ID['boolean'] = TYPE
    ID['any'] = TYPE

    # Special handling for comments
    @_(r'//.*')
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