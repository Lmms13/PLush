from lexer import tokens
import ply.yacc as yacc # type: ignore
parser = yacc.yacc()

#array

# def p_array(p):
#     'array : LBRACKET elements RBRACKET'
#     p[0] = p[2]

# def p_elements(p):
#     '''elements : element COMMA elements
#                 | element'''
#     if len(p) == 4:
#         p[0] = [p[1]] + p[3]
#     else:
#         p[0] = [p[1]]

# def p_element(p):
#     '''element : NUMBER
#                | STRING
#                | CHAR
#                | array'''
#     p[0] = p[1]

# def p_error(p):
#     print("Syntax error at '%s'" % p.value)



#function def
#this is a sketch from copilot, needs to be changed first

# def p_function_definition(p):
#     'function_definition : FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type SEMICOLON body'
#     p[0] = ('function_definition', p[2], p[4], p[7], p[9])

# def p_parameters(p):
#     '''parameters : parameter COMMA parameters
#                   | parameter'''
#     if len(p) == 4:
#         p[0] = [p[1]] + p[3]
#     else:
#         p[0] = [p[1]]

# def p_parameter(p):
#     'parameter : IDENTIFIER COLON type'
#     p[0] = (p[1], p[3])

# def p_type(p):
#     '''type : INT
#             | STRING
#             | LBRACKET type RBRACKET'''
#     if len(p) == 4:
#         p[0] = ('array', p[2])
#     else:
#         p[0] = p[1]

# def p_body(p):
#     'body : statements'
#     p[0] = p[1]



#var and val def
#this is a sketch from copilot, needs to be changed first

# def p_var_definition(p):
#     'var_definition : VAR IDENTIFIER COLON type SEMICOLON'
#     p[0] = ('var_definition', p[2], p[4])

# def p_val_definition(p):
#     'val_definition : VAL IDENTIFIER EQUALS expression SEMICOLON'
#     p[0] = ('val_definition', p[2], p[4])



#arithmetic expressions, might be able to use the ones from main.py in PLY_Simple


#index access
# def p_index_access(p):
#     'index_access : IDENTIFIER LBRACKET expression RBRACKET'
#     p[0] = ('index_access', p[1], p[3])