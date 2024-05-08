from lexer import tokens
from abc import ABC
from dataclasses import dataclass
from typing import Union,List
import ply.yacc as yacc # type: ignore


#statements

class Expression(ABC):
    pass

class Statement(ABC):
    pass

class Declaration(ABC):
    pass

class Definition(ABC):
    pass

@dataclass
class Literal(Expression):
    value: Union[str, int, float, bool] 

@dataclass
class Array(Expression):
    elements: list

@dataclass
class Variable(Expression):
    name: str
    value: Literal
    type: str

@dataclass
class Value(Expression):
    name: str
    value: Literal
    type: str

@dataclass
class FunctionDefinition(Definition):
    name: str
    parameters: List[Union[Variable, Value]]
    return_type: str
    body: List[Statement]

@dataclass
class FunctionDeclaration(Declaration):
    name: str
    parameters: List[Union[Variable, Value]]
    return_type: str

# @dataclass
# class ArrayDefinition(Statement):
#     type: str


#declaration
#definition
#expressions

# dictionary of names
names = { }

start = 'program'


def p_program(p):
    '''program : function_definition
               | array
               | empty'''
    p[0] = p[1]


# Parsing rules

# precedence = (
#     ('left','PLUS','MINUS'),
#     ('left','TIMES','DIVIDE'),
#     ('right','UMINUS'),
#     )

def p_array(p):
    'array : LBRACKET elements RBRACKET'
    p[0] = Array(p[2])

def p_elements(p):
    '''elements : element COMMA elements
                | element'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_element(p):
    '''element : INTEGER
               | FLOAT
               | STRING
               | CHAR
               | array'''
    if isinstance(p[1], list):  # p[1] is an array
        p[0] = p[1]
    elif p[1].isdigit():  # p[1] is an integer
        p[0] = int(p[1])
    else:  # p[1] is a string
        p[0] = p[1].strip()



#array




#function def
#this is a sketch from copilot, needs to be changed first

def p_function_definition(p):
    'function_definition : FUNCTION NAME LPAREN parameters RPAREN COLON type LCURLY body RCURLY'
    names[p[2]] = FunctionDefinition(p[2], p[4], p[7], p[9]) 
    p[0] = names[p[2]]

def p_function_declaration(p):
    'function_definition : FUNCTION NAME LPAREN parameters RPAREN COLON type SEMICOLON'
    names[p[2]] = FunctionDeclaration(p[2], p[4], p[7])
    p[0] = names[p[2]]

def p_parameters(p):
    '''parameters : parameter COMMA parameters
                  | parameter'''
    print(p)
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_parameter(p):
    'parameter : varval NAME COLON type'
    if p[1] == 'var':
        p[0] = Variable(p[2], 1,  p[4])
    else:
        p[0] = Value(p[2], 1, p[4])
    # p[0] = (p[1], p[3])

def p_varval(p):
    '''varval : VAR
              | VAL'''
    p[0] = p[1]

def p_type(p):
    '''type : INTTYPE
            | STRINGTYPE
            | FLOATTYPE
            | CHARTYPE
            | BOOLEANTYPE
            | VOIDTYPE
            | LBRACKET type RBRACKET'''
    if len(p) == 4:
        p[0] = "[" + p[2] + "]"
    else:
        p[0] = p[1]

def p_body(p):
    '''body : statement body
            | empty'''
    p[0] = [Statement()]

def p_statement(p):
    '''statement : INTTYPE'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass


#var and val def
#this is a sketch from copilot, needs to be changed first

# def p_var_definition(p):
#     'var_definition : VAR IDENTIFIER COLON type SEMICOLON'
#     p[0] = ('var_definition', p[2], p[4])

# def p_val_definition(p):
#     'val_definition : VAL IDENTIFIER EQUALS expression SEMICOLON'
#     p[0] = ('val_definition', p[2], p[4])



#arithmetic expressions, might be able to use the ones from main.py in PLY_Simple


# #index access
# def p_index_access(p):
#     'index_access : NAME LBRACKET expression RBRACKET'
#     #p[0] = Literal(p[1], p[3])


parser = yacc.yacc()


while True:
    try:
        s = input('')
    except KeyboardInterrupt:
        break
    # except EOFError:
    #     break
    print(parser.parse(s))
