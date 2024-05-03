
tokens = (
    'STRING','INTEGER','FLOAT','ARRAY','CHAR',
    'AND','OR','NOT',
    'EQUAL','NOTEQUAL','LESS','GREATER','LESSEQUAL','GREATEREQUAL',
    'TRUE','FALSE',
    'ASSIGN','IF','VAR','VAL','FUNCTION','COMMENT','NAME',
    'LCURLY','RCURLY','LBRACKET','RBRACKET','SEMICOLON','LPAREN','RPAREN','COMMA','COLON','HASHTAG',
    'PLUS','MINUS','TIMES','DIVIDE','PERCENT',
    'VOIDTYPE','STRINGTYPE','INTTYPE','FLOATTYPE','CHARTYPE','BOOLEANTYPE'
    )

# Tokens

t_STRING = r'(\"(.|\n|\\)*\")'
t_INTEGER = r'\d(\_|\d)*\d'
t_FLOAT = r'(\d)*\.(\d)+'
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
t_TRUE = r'true'
t_FALSE = r'false'
t_ASSIGN = r':='
t_IF = r'if'
t_VAR = r'var'
t_VAL = r'val'
t_FUNCTION = r'function'
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
t_COMMA = r','
t_COLON = r':'
t_COMMENT = r'\#.*'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_HASHTAG = r'\#'
t_VOIDTYPE= r'void'
t_STRINGTYPE = r'string'
t_INTTYPE = r'int'
t_FLOATTYPE = r'float'
t_CHARTYPE = r'char'
t_BOOLEANTYPE = r'boolean'
#t_ARRAY = r'\[\s*((\d+|(\d*\.\d+)|\'(\\.|[^\'])*\'|\"(\\.|[^\"])*\")(\s*,\s*(\d+|(\d*\.\d+)|\'(\\.|[^\'])*\'|\"(\\.|[^\"])*\"))*)?\s*\]'

# Ignored characters
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex # type: ignore
lexer = lex.lex()

if __name__ == '__main__':
    lexer.input("57_6284692_729")
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)