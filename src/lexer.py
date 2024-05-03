var = 1_2_3
print(var + 3)

# tokens = (
#     'TEXT', 'INTEGER', 'FLOAT', 'ARRAY', 'CHAR'
#     'AND', 'OR', 'NOT', 'EQUAL', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL',
#     'TRUE', 'FALSE',
#     'ASSIGN',
#     'IF', 'VAR', 'VAL', 'FUNCTION', 
#     'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET', 'SEMICOLON', 'LPAREN', 'RPAREN'
#     'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'PERCENT'
# )

# # Tokens

# #t_TEXT = r'[a-zA-Z_][a-zA-Z0-9_]*'
# t_INTEGER = r'(\_)*\d(\_|\d)*'
# t_FLOAT = r'(\d)*\.(\d)+'
# #t_ARRAY = r'\[\]'
# #t_CHAR = r'\d'
# t_AND = r'&&'
# t_OR = r'\|\|'
# t_NOT = r'!'
# t_EQUAL = r'='
# t_NOTEQUAL = r'!='
# t_LESS = r'<'
# t_GREATER = r'>'
# t_LESSEQUAL = r'<='
# t_GREATEREQUAL = r'>='
# t_TRUE = r'true'
# t_FALSE = r'false'
# t_ASSIGN = r':='
# t_IF = r'if'
# t_VAR = r'var'
# t_VAL = r'val'
# t_FUNCTION = r'function'
# t_LCURLY = r'{'
# t_RCURLY = r'}'
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'
# t_SEMICOLON = r';'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_TIMES = r'\*'
# t_DIVIDE = r'/'
# t_PERCENT = r'%'

# import ply.lex as lex
# lexer = lex.lex()

# def t_INTEGER(t):
#     r'(\_)*\d(\_|\d)*'
#     try:
#         t.value = int(t.value)
#     except ValueError:
#         print("Integer value too large %d", t.value)
#         t.value = 0
#     return t