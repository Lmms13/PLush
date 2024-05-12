from plush_parser import *

# print(ast)

# var = Variable("a", Literal(1), "int")

class Context:
    def __init__(self, parent=None):
        self.var_table = {}
        self.function_table = {}
        # self.current_function = None
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

    def set_current_function(self, func):
        self.current_function = func

    def get_current_function(self):
        return self.current_function
    
    def has_name(self, name):
        local_has_name = name in self.var_table or name in self.function_table
        if not local_has_name and self.parent is not None:
            return self.parent.has_name(name)
        else:
            return local_has_name
    
    def set_var(self, name, value):
        if name in self.var_table:
            self.var_table[name].value = value
        elif self.parent is not None:
            self.parent.set_var(name, value)


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []

    def analyze(self):
        for node in self.ast:
            self.visit(node)
        print(self.errors)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print("generic")
        # raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Literal(self, node):
        return(type(node.value))

    def visit_Array(self, node):
        return[self.visit(element) for element in node.elements]
    
    def visit_Variable(self, node):
        print("variable", node.name)

    def visit_Value(self, node):
        print("value", node.name)

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
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("functiondef")
        for statement in node.body:
            self.visit(statement)

    def visit_FunctionDeclaration(self, node):
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("functiondecl")
        for statement in node.body:
            self.visit(statement)
                
    def visit_VariableDefinition(self, node):
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("var_def")
    
    def visit_VariableDeclaration(self, node):
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("var_decl")

    def visit_ValueDefinition(self, node):
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("val_def")

    def visit_ValueDeclaration(self, node):
        # if node.context.has_name(node.var.name):
        #     self.errors.append(f"Variable {node.var.name} already declared")
        # else:
        #     node.context.add_var(node.var)
        print("val_decl")

    def visit_Error(self, node):
        self.errors.append(node.message)
        return None

    def visit_While(self, node):
        if self.visit(node.condition) != bool:
            self.errors.append("The condition of a while statement must be a boolean")
            return None
        else:
            for statement in node.body:
                self.visit(statement)

    def visit_If(self, node):
        if self.visit(node.condition) != bool:
            self.errors.append("The condition of an if statement must be a boolean")
            return None
        else:
            for statement in node.then_block:
                self.visit(statement)
            for statement in node.else_block:
                self.visit(statement)

    def visit_IndexAcess(self, node):
        array = self.visit(node.array)
        index = self.visit(node.index)
        if type(array) != list:
            self.errors.append("Trying to index a non-array")
            return None
        elif type(index) != int:
            self.errors.append("Index must be an integer")
            return None
        else:
            elem_type = self.visit(array[0])
            for element in array:
                if self.visit(element) != elem_type:
                    self.errors.append("All elements of an array must have be of the same type")
                    return None
            return self.visit(array[index])

    def visit_ReturnOrReassign(self, node):
        print("return_or_reassign")
        self.visit(node.value)

    def visit_FunctionCall(self, node):
        print("functioncall", node.name)
        for arg in node.arguments:
            self.visit(arg)

    



    def get_errors(self):
        return self.errors
    
# def verify(ctx, node):
#     sa = SemanticAnalyzer(node)
#     sa.analyze()
#     print(sa.get_errors())
    
# ast = [VariableDeclaration(var.name, var.value), VariableDeclaration(var.name, var.value)]
# print(ast)
fl = 2.2
ast = [Add(Literal(1), Literal(2)), And(Literal(True), Literal(False)), Add(Literal("2"), Literal("2"))]
SemanticAnalyzer(ast).analyze()