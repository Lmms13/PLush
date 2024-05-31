import typing
from plush_parser import *

class Context:
    def __init__(self, parent=None):
        self.var_table = {}
        self.function_table = {}
        self.parent = parent


    def add_var(self, var):
        self.var_table[var.name] = var
    

    def get_var(self, name):
        if name in self.var_table:
            return self.var_table.get(name)
        elif self.parent is not None:
            return self.parent.get_var(name)
        else:
            return None
    

    def add_function(self, func):
        self.function_table[func.name] = func


    def get_function(self, name):
        if name in self.function_table:
            return self.function_table.get(name)
        elif self.parent is not None:
            return self.parent.get_function(name)
        else:
            return None
    

    def has_name(self, name):
        local_has_name = name in self.var_table or name in self.function_table
        return local_has_name
    

    def set_var(self, name, value):
        if name in self.var_table:
            self.var_table[name].value = value
        elif self.parent is not None:
            self.parent.set_var(name, value)


class SemanticAnalyzer:
    def __init__(self, ast, context=[Context()]):
        self.ast = ast
        self.errors = []
        self.context = context


    def analyze(self):
        for node in self.ast:
            self.visit(node)
        if self.errors:
            print("ERRORS:",self.errors)
            return False
        else:
            #print("No semantic errors found")
            return True


    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


    def convert_type(self, type_string):
        if type_string == "int":
                return int
        elif type_string == "float":
                return float
        elif type_string == "string":
                return str
        elif type_string == "boolean":
                return bool
        elif type_string == "char":
                return str
        elif type_string == "void":
                return None
        elif type_string.startswith('[') and type_string.endswith(']'):
                return List[self.convert_type(type_string[1:-1])]


    def find_return_statement(self, node, name, ret_type, missing_return):
        if isinstance(node, ReturnOrReassign):
            if node.name == name:
                missing_return = False
        elif isinstance(node, If):
            for statement in node.then_block:
                missing_return = self.find_return_statement(statement, name, ret_type, missing_return)
                if not missing_return:
                    return False
            for statement in node.else_block:
                missing_return = self.find_return_statement(statement, name, ret_type, missing_return)
                if not missing_return:
                    return False
        elif isinstance(node, While):
            for statement in node.body:
                missing_return = self.find_return_statement(statement, name, ret_type, missing_return)
                if not missing_return:
                    return False
        return missing_return

    def visit_Literal(self, node):
        return(type(node.value))


    def visit_Array(self, node):
        elem_type = self.visit(node.elements[0])
        for element in node.elements:
            if self.visit(element) != elem_type:
                self.errors.append("All elements of an array must be of the same type")
                return None
        return List[elem_type]


    def visit_Variable(self, node):
        if self.context[-1].get_var(node.name) is not None:
            return self.convert_type(self.context[-1].get_var(node.name).type)
        else:
            self.errors.append(f"Variable {node.name} not declared")
            return None


    def visit_Value(self, node):
        if self.context[-1].get_var(node.name) is not None:
            return self.convert_type(self.context[-1].get_var(node.name).type)
        else:
            self.errors.append(f"Value {node.name} not declared")
            return None


    def visit_Add(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on addition")
            return None
        elif self.visit(node.left) == float or self.visit(node.right) == float:
            return float
        else:
            return int


    def visit_Sub(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on subtraction")
            return None
        elif self.visit(node.left) == float or self.visit(node.right) == float:
            return float
        else:
            return int


    def visit_Mul(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on multiplication")
            return None
        elif self.visit(node.left) == float or self.visit(node.right) == float:
            return float
        else:
            return int


    def visit_Div(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on division")
            return None
        else:
            return float


    def visit_Mod(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on modulus")
            return None
        else:
            return int
        
        
    def visit_Power(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on power")
            return None
        elif self.visit(node.left) == int and self.visit(node.right) == int:
            return int
        else:
            return float


    def visit_And(self, node):
        valid = [bool]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on and")
            return None
        else:
            return bool


    def visit_Or(self, node):
        valid = [bool]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on or")
            return None
        else:
            return bool
            
    
    def visit_Not(self, node):
        if self.visit(node.expression) != bool:
            self.errors.append("Incompatible types on not")
            return None
        else:
            return bool


    def visit_Equal(self, node):
        valid = [int, float, str, bool]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on equal")
            return None
        else:
            return bool


    def visit_NotEqual(self, node):
        valid = [int, float, str, bool]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on not equal")
            return None
        else:
            return bool


    def visit_Less(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on less")
            return None
        else:
            return bool


    def visit_Greater(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on greater")
            return None
        else:
            return bool


    def visit_LessEqual(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on less or equal")
            return None
        else:
            return bool


    def visit_GreaterEqual(self, node):
        valid = [int, float]
        if self.visit(node.left) not in valid or self.visit(node.right) not in valid:
            self.errors.append("Incompatible types on greater or equal")
            return None
        else:
            return bool


    def visit_UnaryMinus(self, node):
        valid = [int, float]
        exp_type = self.visit(node.expression)
        if exp_type not in valid:
            self.errors.append("Incompatible types on negation")
            return None
        else:
            return exp_type

 
    def visit_FunctionDefinition(self, node):
        if self.context[-1].has_name(node.name):
            self.errors.append(f"Function or variable with name {node.name} already declared in current scope")
            return None 
        elif node.name == "main" and node.return_type != "void":
            self.errors.append("Main function must have void return type")
            return None
        else:
            self.context[-1].add_function(node)
            self.context.append(Context(self.context[-1]))
            self.context[-1].add_function(node)
            
            if node.arg_num > 0:
                for arg in list(node.local_vars.values())[:node.arg_num]:
                    if self.context[-1].has_name(arg.name):
                        self.errors.append(f"Function arguments must have unique names, {arg.name} is repeated")
                        return None
                    else:
                        self.context[-1].add_var(arg)
            
            missing_return = True
            for statement in node.body:
                if node.return_type == "void":
                    missing_return = False
                else:
                    missing_return = missing_return and self.find_return_statement(statement, node.name, node.return_type, missing_return)
                self.visit(statement)
            
            if missing_return:
                self.errors.append(f"Function {node.name} missing return statement")

            self.context.pop()
            return self.convert_type(node.return_type)


    def visit_FunctionDeclaration(self, node):
        if self.context[-1].has_name(node.name):
            self.errors.append(f"Function or variable with name {node.name} already declared in current scope")
            return None 
        else:
            self.context[-1].add_function(node)
            return self.convert_type(node.return_type)


    def visit_VariableDefinition(self, node):
        if self.context[-1].has_name(node.pointer.name):
            self.errors.append(f"Function or variable with name {node.pointer.name} already declared in current scope")
            return None 
        elif node.pointer.name == "main":
            self.errors.append(f"The name main cannot be used as a variable name")
            return None
        elif node.pointer.type == "void":
            self.errors.append("Variables cannot have void type")
            return None
        elif self.convert_type(node.pointer.type) != self.visit(node.pointer.value):
            self.errors.append(f"Incompatible types on variable definition of {node.pointer.name}")
            return None
        else:
            self.context[-1].add_var(node.pointer)
            return self.visit(node.pointer)


    def visit_VariableDeclaration(self, node):
        if self.context[-1].has_name(node.name):
            self.errors.append(f"Function or variable with name {node.name} already declared in current scope")
            return None 
        elif node.pointer.name == "main":
            self.errors.append(f"The name main cannot be used as a variable name")
            return None
        elif node.type == "void":
            self.errors.append("Variables cannot have void type")
            return None
        else:
            self.context[-1].add_var(node)
            return self.convert_type(node.type)


    def visit_ValueDefinition(self, node):
        if self.context[-1].has_name(node.pointer.name):
            self.errors.append(f"Function or variable with name {node.pointer.name} already declared in current scope")
            return None 
        elif node.pointer.name == "main":
            self.errors.append(f"The name main cannot be used as a value name")
            return None
        elif node.pointer.type == "void":
            self.errors.append("Values cannot have void type")
            return None
        elif self.convert_type(node.pointer.type) != self.visit(node.pointer.value):
            self.errors.append(f"Incompatible types on value definition of {node.pointer.name}")
            return None
        else:
            self.context[-1].add_var(node.pointer)
            return self.visit(node.pointer)


    def visit_ValueDeclaration(self, node):
        if self.context.has_name(node.name):
            self.errors.append(f"Function or variable with name {node.name} already declared in current scope")
            return None 
        elif node.pointer.name == "main":
            self.errors.append(f"The name main cannot be used as a value name")
            return None
        elif node.type == "void":
            self.errors.append("Values cannot have void type")
            return None
        else:
            self.context[-1].add_var(node)
            return self.convert_type(node.type)


    def visit_While(self, node):
        if self.visit(node.condition) != bool:
            self.errors.append("The condition of a while statement must be a boolean")
        else:
            self.context.append(Context(self.context[-1]))
            for statement in node.body:
                self.visit(statement)
            self.context.pop()


    def visit_If(self, node):
        if self.visit(node.condition) != bool:
            self.errors.append("The condition of an if statement must be a boolean")
            return None
        else:
            self.context.append(Context(self.context[-1]))
            for statement in node.then_block:
                self.visit(statement)
            self.context.pop()

            self.context.append(Context(self.context[-1]))
            for statement in node.else_block:
                self.visit(statement)
            self.context.pop()


    def visit_IndexAccess(self, node):
        if self.context[-1].get_var(node.name) is None:
            self.errors.append(F"Trying to index non-existing array {node.name}")
            return None
        elif not (self.context[-1].get_var(node.name).type.startswith('[') and self.context[-1].get_var(node.name).type.endswith(']')):
            self.errors.append(F"Trying to index non-array variable {node.name}")
            return None
        else:
            if isinstance(node.indexes, List):  
                for index in node.indexes:
                    if self.visit(index) != int and self.visit(index) != List[int]:
                        self.errors.append("Index must be an integer")
                        return None
            else:
                if self.visit(node.indexes) != int:
                    self.errors.append("Index must be an integer")
                    return None
            arr = self.context[-1].get_var(node.name)
            num_dimensions = arr.type.count('[')
            return self.convert_type(arr.type[num_dimensions:-num_dimensions])


    def visit_ReturnOrReassign(self, node):
        #if it's an array element reassignment, it's a special case
        #so it needs to be handled before the rest
        if isinstance(node.name, IndexAccess):
            if(len(node.name.indexes) > 1):
                arr_type = self.visit(node.name.indexes[0])
            else:
                arr_type = self.visit(node.name)
            if arr_type != self.visit(node.value):
                self.errors.append("Incompatible types on array element reassignment")
                return None
            elif isinstance(self.context[-1].get_var(node.name.name), Value):
                self.errors.append(F"Cannot reassign constant {node.name.name}")
                return None
            else: 
                return self.visit(node.value)

        #if symbol doesn't exist     
        if self.context[-1].get_function(node.name) is None and self.context[-1].get_var(node.name) is None:
            self.errors.append(f"The symbol {node.name} does not exist")
            return None
        
        #if it's a return statement
        elif self.context[-1].get_function(node.name) is not None:
            if len(self.context) == 1:
                self.errors.append("Return statement outside of function scope")
                return None
            elif self.context[-1].get_function(node.name).return_type == "void" and node.value is not None:
                self.errors.append("Function with void return type cannot return a value")
                return None
            elif self.context[-1].get_function(node.name).return_type == "void" and node.value is None:
                return self.convert_type(self.context[-1].get_function(node.name).return_type)
            elif self.convert_type(self.context[-1].get_function(node.name).return_type) != self.visit(node.value):
                self.errors.append(f"Incompatible types on return of function {node.name}")
                return None
            else:
                return self.visit(node.value)
        
        #if it's a reassignment
        elif self.context[-1].get_var(node.name) is None:
            self.errors.append(f"Trying to reassign non-existing variable {node.name}")
            return None
        elif self.convert_type(self.context[-1].get_var(node.name).type) != self.visit(node.value):
            self.errors.append(f"Incompatible types on reassignment of {node.name}")
            return None
        elif isinstance(self.context[-1].get_var(node.name), Value):
            self.errors.append(f"Cannot reassign constant {node.name}")
            return None
        else:
            self.context[-1].set_var(node.name, node.value)
            return self.visit(node.value)


    def visit_FunctionCall(self, node):
        if len(self.context) == 1:
            self.errors.append("Function calls outside of function scope are not allowed")
            return None
        elif node.name == "main":
            self.errors.append("Cannot call main function")
            return None
        elif self.context[-1].get_function(node.name) is None:
            self.errors.append(f"Function {node.name} not declared")
            return None
        elif len(node.arguments) != self.context[-1].get_function(node.name).arg_num:
            self.errors.append(f"Function {node.name} called with the wrong number of arguments")
            return None
        else:
            args = list(self.context[-1].get_function(node.name).local_vars.values())[:len(node.arguments)]
            for i, arg in enumerate(node.arguments):
                if isinstance(arg, IndexAccess):
                    if len(arg.indexes) > 1:
                        if self.visit(arg.indexes[0]) != self.convert_type(args[i].type):
                            self.errors.append(f"Type mismatch in function call of {node.name}")
                            return None  
                elif self.visit(arg) != self.convert_type(args[i].type):
                    self.errors.append(f"Type mismatch in function call of {node.name}")
                    return None
            return self.convert_type(self.context[-1].get_function(node.name).return_type)


    def visit_Error(self, node):
        self.errors.append(node.message)
        return None
    

    def get_errors(self):
        return self.errors