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
class Add(Expression):
    left: Expression
    right: Expression

@dataclass
class Sub(Expression):
    left: Expression
    right: Expression

@dataclass
class Mul(Expression):
    left: Expression
    right: Expression

@dataclass
class Div(Expression):
    left: Expression
    right: Expression

@dataclass
class Mod(Expression):
    left: Expression
    right: Expression

@dataclass
class And(Expression):
    left: Expression
    right: Expression

@dataclass
class Or(Expression):
    left: Expression
    right: Expression

@dataclass
class Not(Expression):
    expression: Expression

@dataclass
class Equal(Expression):
    left: Expression
    right: Expression

@dataclass
class NotEqual(Expression):
    left: Expression
    right: Expression

@dataclass
class Less(Expression):
    left: Expression
    right: Expression

@dataclass
class Greater(Expression):
    left: Expression
    right: Expression

@dataclass
class LessEqual(Expression):
    left: Expression
    right: Expression

@dataclass
class GreaterEqual(Expression):
    left: Expression
    right: Expression

@dataclass
class UnaryMinus(Expression):
    expression: Expression

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
class IndexAcess(Expression):
    array: Union[Variable,Value]
    index: Expression

@dataclass
class ReturnOrReassign(Statement):
    name: Union[str,IndexAcess]
    value: Expression

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]

# @dataclass
# class NonEvaluatedExpression(Expression):
#     name1: str
#     name2: str
#     value: Union[Literal,Array]
#     operator: str

# @dataclass
# class Test(Expression):
#     p: str

names = { }

# functions = {}

# curr_func = []


start = 'program'


def p_program(p):
    '''program : statement_list
               | empty'''
    p[0] = p[1]

def p_statement_list_1(p):
    '''statement_list : statement statement_list'''
    p[0] = [p[1]] + p[2]

def p_statement_list_2(p):
    '''statement_list : statement'''
    p[0] = [p[1]]

def p_statement(p):
    '''statement : function_definition
                 | function_declaration
                 | variable_definition
                 | variable_declaration
                 | value_definition
                 | value_declaration
                 | expression SEMICOLON
                 | return_or_reassign_statement'''
    p[0] = p[1]

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
    if isinstance(p[1], list):
        p[0] = p[1]
    elif p[1].isdigit(): 
        p[0] = int(p[1])
    else:
        p[0] = p[1].strip()



#var

def p_variable_definition(p):
    '''variable_definition : VAR NAME COLON type ASSIGN expression SEMICOLON
                           | VAR NAME COLON type ASSIGN array SEMICOLON'''
    p[0] = VariableDefinition(Variable(p[2], p[6], p[4]))

def p_variable_declaration(p):
    'variable_declaration : VAR NAME COLON type SEMICOLON'
    p[0] = VariableDeclaration(p[2], p[4])

def p_value_definition(p):
    '''value_definition : VAL NAME COLON type ASSIGN expression SEMICOLON
                        | VAL NAME COLON type ASSIGN array SEMICOLON'''
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
   
    # if(isinstance(p[1], Test) or isinstance(p[3], Test)):
    #     if(isinstance(p[1], Test) and not isinstance(p[3], Test)):
    #         p[0] = Test(p[1].p + p[2] + str(p[3].value))
    #     elif(isinstance(p[3], Test) and not isinstance(p[1], Test)):
    #         p[0] = Test(str(p[1].value) + p[2] + p[3].p)
    #     else:
    #         p[0] = Test(p[1].p + p[2] + p[3].p)
            
        
    # elif type(p[1].value) == str or type(p[3].value) == str:
    #     p[0] = Error("Unsupported operation")
    if p[2] == '+':
        p[0] = Add(p[1], p[3])
    elif p[2] == '-':
        p[0] = Sub(p[1], p[3])
    elif p[2] == '*':
        p[0] = Mul(p[1], p[3])
    elif p[2] == '/':
        p[0] = Div(p[1], p[3])
    elif p[2] == '%':
        p[0] = Mod(p[1], p[3])
    elif p[2] == '&&':
        p[0] = And(p[1], p[3])
    elif p[2] == '||':
        p[0] = Or(p[1], p[3])
    elif p[2] == '=':
        p[0] = Equal(p[1], p[3])
    elif p[2] == '!=':
        p[0] = NotEqual(p[1], p[3])
    elif p[2] == '<':
        p[0] = Less(p[1], p[3])
    elif p[2] == '>':
        p[0] = Greater(p[1], p[3])
    elif p[2] == '<=':
        p[0] = LessEqual(p[1], p[3])
    elif p[2] == '>=':
        p[0] = GreaterEqual(p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryMinus(p[2])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = Not(p[2])

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
        p[0] = Variable(p[1], None, None)
    else:
        p[0] = Variable(p[1], None, None)


def p_function_definition(p):
    '''function_definition : FUNCTION NAME LPAREN parameters RPAREN COLON type LCURLY body RCURLY
                           | FUNCTION NAME LPAREN parameters RPAREN LCURLY body RCURLY'''
    if len(p) == 11:
        func = FunctionDefinition(p[2], p[4], p[7], p[9])
    else:
        func = FunctionDefinition(p[2], p[4], 'void', p[7])
    for s in func.body:
        if isinstance(s, VariableDefinition) or isinstance(s, ValueDefinition):
            func.local_vars[s.pointer.name] = s.pointer
   
   # for i, s in enumerate(func.body):
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
        
        
        # if isinstance(s, Test):
        #     split = re.split((r"(\+|-|\*|/|%|&&|\|\||=|!=|<|>|<=|>=|!)"),s.p)
        #     varss = {}
        #     for a in split:
        #         a = re.sub(r"\(|\)", "", a)
        #         if a in func.local_vars:
        #             varss[a] = func.local_vars[a].value.value
        #     s.p = re.sub(r"!", "not ", s.p)
        #     s.p = re.sub(r"&&", " and ", s.p)
        #     s.p = re.sub(r"\|\|", " or ", s.p)
        #     s.p = re.sub(r"=", "==", s.p)
        #     func.body[i] = Literal(eval(s.p, names, varss))


            
    #functions[p[2]] = func
    p[0] = func

def p_function_declaration(p):
    '''function_declaration : FUNCTION NAME LPAREN parameters RPAREN COLON type SEMICOLON
                            | FUNCTION NAME LPAREN parameters RPAREN SEMICOLON'''
    if len(p) == 9:
        p[0] = FunctionDeclaration(p[2], p[4], p[7])
    else:
        p[0] = FunctionDeclaration(p[2], p[4], 'void')

def p_return_or_reassign_statement(p):
    '''return_or_reassign_statement : NAME ASSIGN expression SEMICOLON
                                    | NAME LBRACKET expression RBRACKET ASSIGN expression SEMICOLON'''
    if len(p) == 5:
        p[0] = ReturnOrReassign(p[1], p[3])
    else:
        p[0] = ReturnOrReassign(IndexAcess(p[1], p[3]), p[6])


def p_parameters(p):
    '''parameters : parameter COMMA parameters
                  | parameter
                  | empty'''
    params = {}
    if p[1] is not None:
        params.update(dict([p[1]]))
        if len(p) == 4:
            params.update(p[3])
    p[0] = params 

def p_parameter(p):
    'parameter : varval NAME COLON type'
    if p[1] == 'var':
        p[0] = (p[2], Variable(p[2], None,  p[4]))
    else:
        p[0] = (p[2], Value(p[2], None, p[4]))

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
            | LBRACKET type_no_void RBRACKET'''
    if len(p) == 4:
        p[0] = "[" + p[2] + "]"
    else:
        p[0] = p[1]

def p_type_no_void(p):
    '''type_no_void : INTTYPE
                    | STRINGTYPE
                    | FLOATTYPE
                    | CHARTYPE
                    | BOOLEANTYPE
                    | LBRACKET type_no_void RBRACKET'''
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

def p_expression_function_call(p):
    'expression : NAME LPAREN arguments RPAREN'
    p[0] = FunctionCall(p[1], p[3])

def p_arguments(p):
    '''arguments : argument COMMA arguments
                 | argument
                 | empty'''
    if p[1] is not None:
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    else:
        p[0] = []

def p_argument(p):
    'argument : expression'
    p[0] = p[1]

def p_if_statement(p):
    '''statement : IF expression LCURLY body RCURLY
                 | IF expression LCURLY body RCURLY ELSE LCURLY body RCURLY'''
    if len(p) == 6:
        p[0] = If(p[2], p[4], [])
    else:
        p[0] = If(p[2], p[4], p[9])

def p_while_statement(p):
    'statement : WHILE expression LCURLY body RCURLY'
    p[0] = While(p[2], p[4])

def p_empty(p):
    'empty : '
    pass

def p_expression_index_access(p):
    'expression : NAME LBRACKET expression RBRACKET'
    p[0] = IndexAcess(p[1], p[3])


parser = yacc.yacc()

ast = []

# while True:
#     try:
#         s = input('')
#     except KeyboardInterrupt:
#         print(ast)
#         break
#     # except EOFError:
#     #     break
#     print(parser.parse(s))
#     ast.append(parser.parse(s))

with open('../test/0_valid/maxRangeSquared.pl', 'r') as file:
    data = file.read()

result = parser.parse(data)
ast.append(result)

print(ast)

#error handling