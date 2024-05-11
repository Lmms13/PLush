from lexer import tokens
from abc import ABC
from dataclasses import dataclass
from typing import Union,List,Dict
import ply.yacc as yacc # type: ignore
import re


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
    value: Union[Literal,Array]
    type: str

@dataclass
class Value(Expression):
    name: str
    value: Union[Literal,Array]
    type: str

@dataclass
class FunctionDefinition(Definition):
    name: str
    local_vars: Dict[str, Union[Variable, Value]]
    return_type: str
    body: List[Statement]

@dataclass
class FunctionDeclaration(Declaration):
    name: str
    local_vars: Dict[str, Union[Variable, Value]]
    return_type: str

@dataclass
class VariableDefinition(Definition):
    pointer: Variable

@dataclass
class VariableDeclaration(Declaration):
    name: str
    type: str

@dataclass
class ValueDefinition(Definition):
    pointer: Value

@dataclass
class ValueDeclaration(Declaration):
    name: str
    type: str

@dataclass
class Error(Expression):
    message: str

@dataclass
class While(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class If(Statement):
    condition: Expression
    then_block: List[Statement]
    else_block: List[Statement]

@dataclass
class NonEvaluatedExpression(Expression):
    name1: str
    name2: str
    value: Union[Literal,Array]
    operator: str

@dataclass
class Test(Expression):
    p: str


#declaration
#definition
#expressions

# dictionary of names
names = { }

functions = {}

curr_func = []


start = 'program'


def p_program(p):
    '''program : function_definition
                | function_declaration
                | variable_definition
                | variable_declaration
                | value_definition
                | value_declaration
                | statement
                | empty'''
    p[0] = p[1] #remove array after


# Parsing rules

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

def p_array_definition(p):
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
               | TRUE
               | FALSE
               | array'''
    if isinstance(p[1], list):  # p[1] is an array
        p[0] = p[1]
    elif p[1].isdigit():  # p[1] is an integer
        p[0] = int(p[1])
    else:  # p[1] is a string
        p[0] = p[1].strip()



#var

def p_variable_definition(p):
    '''variable_definition : VAR NAME COLON type ASSIGN expression SEMICOLON
                           | VAR NAME COLON type ASSIGN array SEMICOLON'''
    names[p[2]] = VariableDefinition(Variable(p[2], p[6], p[4]))
    p[0] = VariableDefinition(Variable(p[2], p[6], p[4]))

def p_variable_declaration(p):
    'variable_declaration : VAR NAME COLON type SEMICOLON'
    p[0] = VariableDeclaration(p[2], p[4])

def p_value_definition(p):
    '''value_definition : VAL NAME COLON type ASSIGN expression SEMICOLON
                        | VAL NAME COLON type ASSIGN array SEMICOLON'''
    names[p[2]] = ValueDefinition(Value(p[2], p[6], p[4]))
    p[0] = ValueDefinition(Value(p[2], p[6], p[4]))

def p_value_declaration(p):
    'value_declaration : VAL NAME COLON type SEMICOLON'
    p[0] = ValueDeclaration(p[2], p[4])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression PERCENT expression
                    | expression AND expression
                    | expression OR expression
                    | expression EQUAL expression
                    | expression NOTEQUAL expression
                    | expression LESS expression
                    | expression GREATER expression
                    | expression LESSEQUAL expression
                    | expression GREATEREQUAL expression'''
    
    # if(isinstance(p[1], NonEvaluatedExpression) or isinstance(p[3], NonEvaluatedExpression)):
    #     if(isinstance(p[1], NonEvaluatedExpression) and not isinstance(p[3], NonEvaluatedExpression)):
    #         p[0] = NonEvaluatedExpression(p[1].name1, None, p[3].value, p[2])
    #     elif(isinstance(p[3], NonEvaluatedExpression) and not isinstance(p[1], NonEvaluatedExpression)):
    #         p[0] = NonEvaluatedExpression(None, p[1].name1, p[1].value, p[2])
    #     else:
    #         p[0] = NonEvaluatedExpression(p[1].name1, p[3].name1 , None, p[2])
    if(isinstance(p[1], Test) or isinstance(p[3], Test)):
        if(isinstance(p[1], Test) and not isinstance(p[3], Test)):
            p[0] = Test(p[1].p + p[2] + str(p[3].value))
        elif(isinstance(p[3], Test) and not isinstance(p[1], Test)):
            p[0] = Test(str(p[1].value) + p[2] + p[3].p)
        else:
            p[0] = Test(p[1].p + p[2] + p[3].p)
            
        
    # elif type(p[1].value) == str or type(p[3].value) == str:
    #     p[0] = Error("Unsupported operation")
    elif p[2] == '+':
        p[0] = Literal(p[1].value + p[3].value)
    elif p[2] == '-':
        p[0] = Literal(p[1].value - p[3].value)
    elif p[2] == '*':
        p[0] = Literal(p[1].value * p[3].value)
    elif p[2] == '/':
        p[0] = Literal(p[1].value / p[3].value)
    elif p[2] == '%':
        p[0] = Literal(p[1].value % p[3].value)
    elif p[2] == '&&':
        p[0] = Literal(p[1].value and p[3].value)
    elif p[2] == '||':
        p[0] = Literal(p[1].value or p[3].value)
    elif p[2] == '=':
        p[0] = Literal(p[1].value == p[3].value)
    elif p[2] == '!=':
        p[0] = Literal(p[1].value != p[3].value)
    elif p[2] == '<':
        p[0] = Literal(p[1].value < p[3].value)
    elif p[2] == '>':
        p[0] = Literal(p[1].value > p[3].value)
    elif p[2] == '<=':
        p[0] = Literal(p[1].value <= p[3].value)
    elif p[2] == '>=':
        p[0] = Literal(p[1].value >= p[3].value)

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    if(isinstance(p[2], Test)):
        p[0] = Test(p[1] + p[2].p + p[3])
    else:
        p[0] = p[2]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    if(isinstance(p[2], Test)):
        p[0] = Test("-" + p[2].p)
    elif(isinstance(p[2], str)):
        p[0] = Literal(-int(p[2].value))
    else:
        p[0] = Literal(-p[2].value)

def p_expression_not(p):
    'expression : NOT expression'
    if(isinstance(p[2], Test)):
        p[0] = Test("!" + p[2].p)
    else:
        p[0] = Literal(not p[2].value)

def p_expression_literal(p):
    '''expression : INTEGER
                    | FLOAT
                    | STRING
                    | CHAR
                    | TRUE
                    | FALSE'''
    
    if isinstance (p[1], float):
        p[0] = Literal(p[1])
    elif p[1].isdigit():
        p[0] = Literal(int(p[1]))
    elif p[1].lower() == "true":
        p[0] = Literal(True)
    elif p[1].lower() == "false":
        p[0] = Literal(False)
    else:
        p[0] = Literal(p[1])

def p_expression_name(p):
    'expression : NAME'
    if p[1] in names:
        p[0] = names[p[1]].pointer.value
    else:
        #p[0] = NonEvaluatedExpression(p[1], None, None, None)
        p[0] = Test(p[1])
    # else:
    #     p[0] = Error("Undefined name '%s'" % p[1])

#function def
#this is a sketch from copilot, needs to be changed first

def p_function_definition(p):
    'function_definition : FUNCTION NAME LPAREN parameters RPAREN COLON type LCURLY body RCURLY'
    func = FunctionDefinition(p[2], p[4], p[7], p[9])
    for s in func.body:
        if isinstance(s, VariableDefinition) or isinstance(s, ValueDefinition):
            func.local_vars[s.pointer.name] = s.pointer
    
    #this shit has NO error handling, the same for p_expression_name 
    #and p_expression, gotta fix that
    #also this doesn't handle unary operators
    #and it doesn't handle multiple operands
    for i, s in enumerate(func.body):
        # if isinstance(s, NonEvaluatedExpression):
        #     vars = []
        #     if s.name1 in func.local_vars or s.name2 in func.local_vars:     
        #         if(s.name1 in func.local_vars and s.name2 not in func.local_vars):
        #             vars += [func.local_vars[s.name1].value]
        #             vars += [s.value]
        #         elif(s.name2 in func.local_vars and s.name1 not in func.local_vars):
        #             vars += [func.local_vars[s.name2].value]
        #             vars += [s.value]
        #         else:
        #             vars += [func.local_vars[s.name1].value]
        #             vars += [func.local_vars[s.name2].value]

        #         if s.operator == '+':
        #             func.body[i] = Literal(vars[0].value + vars[1].value)
        #         elif s.operator == '-':
        #             func.body[i] = Literal(vars[0].value - vars[1].value)
        #         elif s.operator == '*':
        #             func.body[i] = Literal(vars[0].value * vars[1].value)
        #         elif s.operator == '/':
        #             func.body[i] = Literal(vars[0].value / vars[1].value)
        #         elif s.operator == '%':
        #             func.body[i] = Literal(vars[0].value % vars[1].value)
        #         elif s.operator == '&&':
        #             func.body[i] = Literal(vars[0].value and vars[1].value)
        #         elif s.operator == '||':
        #             func.body[i] = Literal(vars[0].value or vars[1].value)
        #         elif s.operator == '=':
        #             func.body[i] = Literal(vars[0].value == vars[1].value)
        #         elif s.operator == '!=':
        #             func.body[i] = Literal(vars[0].value != vars[1].value)
        #         elif s.operator == '<':
        #             func.body[i] = Literal(vars[0].value < vars[1].value)
        #         elif s.operator == '>':
        #             func.body[i] = Literal(vars[0].value > vars[1].value)
        #         elif s.operator == '<=':
        #             func.body[i] = Literal(vars[0].value <= vars[1].value)
        #         elif s.operator == '>=':
        #             func.body[i] = Literal(vars[0].value >= vars[1].value)
        if isinstance(s, Test):
            split = re.split((r"(\+|-|\*|/|%|&&|\|\||=|!=|<|>|<=|>=|!)"),s.p)
            varss = {}
            for a in split:
                a = re.sub(r"\(|\)", "", a)
                if a in func.local_vars:
                    varss[a] = func.local_vars[a].value.value
            s.p = re.sub(r"!", "not ", s.p)
            s.p = re.sub(r"&&", " and ", s.p)
            s.p = re.sub(r"\|\|", " or ", s.p)
            s.p = re.sub(r"=", "==", s.p)
            func.body[i] = Literal(eval(s.p, names, varss))


            
    functions[p[2]] = func
    p[0] = func

def p_function_declaration(p):
    'function_declaration : FUNCTION NAME LPAREN parameters RPAREN COLON type SEMICOLON'
    functions[p[2]] = FunctionDeclaration(p[2], p[4], p[7])
    p[0] = functions[p[2]]

def p_parameters(p):
    '''parameters : parameter COMMA parameters
                  | parameter'''
    params = {}
    data = list()
    if len(p) == 4:
        data = [p[1]] + p[3]
    else:
        data = [p[1]]
    params.update(data)
    p[0] = params 

def p_parameter(p):
    'parameter : varval NAME COLON type'
    if p[1] == 'var':
        p[0] = (p[2], Variable(p[2], Literal(1),  p[4]))
    else:
        p[0] = (p[2], Value(p[2], Literal(1), p[4]))

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
    if p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement : expression SEMICOLON
                 | variable_definition_in_func
                 | value_definition_in_func'''
    p[0] = p[1]


def p_variable_definition_in_func(p):
    '''variable_definition_in_func : VAR NAME COLON type ASSIGN expression SEMICOLON
                                   | VAR NAME COLON type ASSIGN array SEMICOLON'''
    p[0] = VariableDefinition(Variable(p[2], p[6], p[4]))

def p_value_definition_in_func(p):
    '''value_definition_in_func : VAL NAME COLON type ASSIGN expression SEMICOLON
                                | VAL NAME COLON type ASSIGN array SEMICOLON'''
    p[0] = ValueDefinition(Value(p[2], p[6], p[4]))

def p_empty(p):
    'empty :'
    pass




#arithmetic expressions, might be able to use the ones from main.py in PLY_Simple


#index access
def p_expression_index_access(p):
    'expression : NAME LBRACKET expression RBRACKET'
    p[0] = names[p[1]].pointer.value.elements[p[3].value]


parser = yacc.yacc()


while True:
    try:
        s = input('')
    except KeyboardInterrupt:
        break
    # except EOFError:
    #     break
    print(parser.parse(s))


#reassign var values
#if statements
#while loops
#double check statements
#error handling
#parameters are being initialized as 1, look into that
    #function calls ^