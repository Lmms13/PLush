tokens = (
    'STRING','INTEGER','FLOAT','CHAR',
    'AND','OR','NOT',
    'EQUAL','NOTEQUAL','LESS','GREATER','LESSEQUAL','GREATEREQUAL',
    'TRUE','FALSE',
    'ASSIGN','IF','ELSE','VAR','VAL','FUNCTION','COMMENT','NAME','WHILE',
    'LCURLY','RCURLY','LBRACKET','RBRACKET','SEMICOLON','LPAREN','RPAREN','COMMA','COLON',
    'PLUS','MINUS','TIMES','DIVIDE','PERCENT','POWER',
    'VOIDTYPE','STRINGTYPE','INTTYPE','FLOATTYPE','CHARTYPE','BOOLEANTYPE'
    )

reserved = {    
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'var': 'VAR',
    'val': 'VAL',
    'function': 'FUNCTION',
    'void': 'VOIDTYPE',
    'string': 'STRINGTYPE',
    'int': 'INTTYPE',
    'float': 'FLOATTYPE',
    'char': 'CHARTYPE',
    'boolean': 'BOOLEANTYPE'
}

t_CHAR = r'(\'\d\'|\"\d\")'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_EQUAL = r'='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_ASSIGN = r':='
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PERCENT = r'%'
t_POWER = r'\^'
t_COMMA = r','
t_COLON = r':'

t_ignore = " \t\n"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

def t_COMMENT(t):
    r'\#.*'
    pass

def t_FLOAT(t):
    r'(\d)*\.(\d)+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value.replace("\"","")
    return t

def t_INTEGER(t):
    r'\d((\_|\d)*\d)?'
    t.value = t.value.replace("_","")
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:     
        return globals()["t_" + reserved[t.value]](t)
    else:
        return t

def t_FUNCTION(t): 
    r'function'
    t.type = 'FUNCTION'
    return t

def t_VAR(t):
    r'var'
    t.type = 'VAR'
    return t

def t_VAL(t):
    r'val'
    t.type = 'VAL'
    return t

def t_INTTYPE(t):
    r'int'
    t.type = 'INTTYPE'
    return t

def t_FLOATTYPE(t): 
    r'float'
    t.type = 'FLOATTYPE'
    return t    

def t_STRINGTYPE(t):
    r'string'
    t.type = 'STRINGTYPE'
    return t

def t_CHARTYPE(t):
    r'char'
    t.type = 'CHARTYPE'
    return t

def t_BOOLEANTYPE(t):
    r'boolean'
    t.type = 'BOOLEANTYPE'
    return t

def t_VOIDTYPE(t):
    r'void'
    t.type = 'VOIDTYPE'
    return t

def t_TRUE(t):
    r'true'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'false'
    t.type = 'FALSE'
    return t

def t_IF(t):
    r'if'
    t.type = 'IF'
    return t

def t_ELSE(t):
    r'else'
    t.type = 'ELSE'
    return t

def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    return t

err = False

def t_error(t):
    global err
    err = True
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex # type: ignore
lexer = lex.lex()

if __name__ == '__main__':
    filepath = '../test/0_valid/validTest.pl'
    with open(filepath, 'r') as file:
        for line in file:
            lexer.input(line)
            while True:
                tok = lexer.token()
                if not tok: 
                    break  # No more input
    if not err:
        print("All tokens are valid")