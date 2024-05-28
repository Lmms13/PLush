from plush_parser import *

# filepath = '../test/0_valid/countOccurrences.pl'
# with open(filepath, 'r') as file:
#     data = file.read()

# ast = parse_data(data)

class CodeGenerator:

    context = ""

    def generate(self, ast):
        code = "#include <stdio.h>\n#include <math.h>\n\n"
        for node in ast:
            code += self.generate_C_code(node)
        return code
    
    def generate_C_code(self, node):
        if isinstance(node, Literal):
            return self.generate_C_code_Literal(node)
        elif isinstance(node, Array):
            return self.generate_C_code_Array(node)
        elif isinstance(node, Variable):
            return self.generate_C_code_Variable(node)
        elif isinstance(node, Value):
            return self.generate_C_code_Value(node)
        elif isinstance(node, Add):
            return self.generate_C_code_Add(node)
        elif isinstance(node, Sub):
            return self.generate_C_code_Sub(node)
        elif isinstance(node, Mul):
            return self.generate_C_code_Mul(node)
        elif isinstance(node, Div):
            return self.generate_C_code_Div(node)
        elif isinstance(node, Mod):
            return self.generate_C_code_Mod(node)
        elif isinstance(node, Power):
            return self.generate_C_code_Power(node)
        elif isinstance(node, And):
            return self.generate_C_code_And(node)
        elif isinstance(node, Or):
            return self.generate_C_code_Or(node)
        elif isinstance(node, Not):
            return self.generate_C_code_Not(node)
        elif isinstance(node, Equal):
            return self.generate_C_code_Equal(node)
        elif isinstance(node, NotEqual):
            return self.generate_C_code_NotEqual(node)
        elif isinstance(node, Less):
            return self.generate_C_code_Less(node)
        elif isinstance(node, Greater):
            return self.generate_C_code_Greater(node)
        elif isinstance(node, LessEqual):
            return self.generate_C_code_LessEqual(node)
        elif isinstance(node, GreaterEqual):
            return self.generate_C_code_GreaterEqual(node)
        elif isinstance(node, UnaryMinus):
            return self.generate_C_code_UnaryMinus(node)
        elif isinstance(node, FunctionDefinition):
            return self.generate_C_code_FunctionDefinition(node)
        elif isinstance(node, FunctionDeclaration):
            return self.generate_C_code_FunctionDeclaration(node)
        elif isinstance(node, VariableDefinition):
            return self.generate_C_code_VariableDefinition(node)
        elif isinstance(node, VariableDeclaration):
            return self.generate_C_code_VariableDeclaration(node)
        elif isinstance(node, ValueDefinition):
            return self.generate_C_code_ValueDefinition(node)
        elif isinstance(node, ValueDeclaration):
            return self.generate_C_code_ValueDeclaration(node)
        elif isinstance(node, While):
            return self.generate_C_code_While(node)
        elif isinstance(node, If):
            return self.generate_C_code_If(node)
        elif isinstance(node, IndexAccess):
            return self.generate_C_code_IndexAccess(node)
        elif isinstance(node, ReturnOrReassign):
            return self.generate_C_code_ReturnOrReassign(node)
        elif isinstance(node, FunctionCall):
            return self.generate_C_code_FunctionCall(node)
        elif isinstance(node, Error):
            return self.generate_C_code_Error(node)
        else:
            return ""

    def generate_C_code_Literal(self, node):
        return f"{node.value}"

    def generate_C_code_Array(self, node):
        code = "{"
        for i, element in enumerate(node.elements):
            code += self.generate_C_code(element)
            if i < len(node.elements) - 1:
                code += ", "
        code += "}"
        return code

    def generate_C_code_Variable(self, node):
        return f"{node.name}"

    def generate_C_code_Value(self, node):
        return f"{node.value}"

    def generate_C_code_Add(self, node):
        return f"{self.generate_C_code(node.left)} + {self.generate_C_code(node.right)}"

    def generate_C_code_Sub(self, node):
        return f"{self.generate_C_code(node.left)} - {self.generate_C_code(node.right)}"

    def generate_C_code_Mul(self, node):
        return f"{self.generate_C_code(node.left)} * {self.generate_C_code(node.right)}"

    def generate_C_code_Div(self, node):
        return f"{self.generate_C_code(node.left)} / {self.generate_C_code(node.right)}"

    def generate_C_code_Mod(self, node):
        return f"{self.generate_C_code(node.left)} % {self.generate_C_code(node.right)}"

    def generate_C_code_Power(self, node):
        if type(node.left.value) == int and type(node.right.value) == int:
            return f"(int) pow({self.generate_C_code(node.left)}, {self.generate_C_code(node.right)})"
        else:
            return f"pow({self.generate_C_code(node.left)}, {self.generate_C_code(node.right)})"

    def generate_C_code_And(self, node):
        return f"{self.generate_C_code(node.left)} && {self.generate_C_code(node.right)}"

    def generate_C_code_Or(self, node):
        return f"{self.generate_C_code(node.left)} || {self.generate_C_code(node.right)}"

    def generate_C_code_Not(self, node):
        return f"!{self.generate_C_code(node.expression)}"

    def generate_C_code_Equal(self, node):
        return f"{self.generate_C_code(node.left)} == {self.generate_C_code(node.right)}"

    def generate_C_code_NotEqual(self, node):
        return f"{self.generate_C_code(node.left)} != {self.generate_C_code(node.right)}"

    def generate_C_code_Less(self, node):
        return f"{self.generate_C_code(node.left)} < {self.generate_C_code(node.right)}"

    def generate_C_code_Greater(self, node):
        return f"{self.generate_C_code(node.left)} > {self.generate_C_code(node.right)}"

    def generate_C_code_LessEqual(self, node):
        return f"{self.generate_C_code(node.left)} <= {self.generate_C_code(node.right)}"

    def generate_C_code_GreaterEqual(self, node):
        return f"{self.generate_C_code(node.left)} >= {self.generate_C_code(node.right)}"

    def generate_C_code_UnaryMinus(self, node):
        return f"-{self.generate_C_code(node.expression)}"

    def generate_C_code_FunctionDefinition(self, node):
        if(node.name == "main"):
            code = f"int main(int argc, char *argv[]) {{\n"                                                   
        else:
            code = f"{self.compute_return_type(node.return_type)} {node.name}("
            if node.arg_num > 0:
                for i, arg in enumerate(list(node.local_vars.values())[:node.arg_num]):
                    # if arg.type.startswith("["):
                    #     if arg.type[1:-1] == "string":
                    #         code += f"char {arg.name}[]"
                    #     else:
                    #         code += f"{arg.type[1:-1]} {arg.name}[]"
                    # elif arg.type == "string":
                    #     code += f"char {arg.name}[]"
                    # else:
                    #     code += f"{arg.type} {arg.name}"
                    code += f"{self.compute_type(arg.type, arg.name)}"
                    if i < node.arg_num - 1:
                        code += ", "
            code += ") {\n"

        self.context = node.name
        for statement in node.body:
            code += "\t" + self.generate_C_code(statement)
    
        if(node.name == "main"):
            code += "\treturn 0;\n"
        code += "}\n"
        self.context = ""

        return code

    def generate_C_code_FunctionDeclaration(self, node):
        code = f"{self.compute_return_type(node.return_type)} {node.name}("
        if node.arg_num > 0:
            for i, arg in enumerate(list(node.local_vars.values())[:node.arg_num]):
                # if arg.type.startswith("["):
                #     if arg.type[1:-1] == "string":
                #         code += f"char {arg.name}[]"
                #     else:
                #         code += f"{arg.type[1:-1]} {arg.name}[]"
                # elif arg.type == "string":
                #     code += f"char {arg.name}[]"
                #else:
                    #code += f"{arg.type} {arg.name}"
                code += f"{self.compute_type(arg.type, arg.name)}"
                if i < node.arg_num - 1:
                    code += ", "
        code += ");\n"
        return code

    def generate_C_code_VariableDefinition(self, node):
        # if node.pointer.type.startswith("["):
        #     if node.pointer.type[1:-1] == "string":
        #         return f"char {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        #     else:
        #         return f"{node.pointer.type[1:-1]} {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        # elif node.pointer.type == "string":
        #     return f"char {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        # return f"{node.pointer.type} {node.pointer.name} = {self.generate_C_code(node.pointer.value)};\n"
        return f"{self.compute_type(node.pointer.type, node.pointer.name)} = {self.generate_C_code(node.pointer.value)};\n"


    def generate_C_code_VariableDeclaration(self, node):
        # if node.type.startswith("["):
        #     if node.type[1:-1] == "string":
        #         return f"char {node.name}[];\n"
        #     else:
        #         return f"{node.type[1:-1]} {node.name}[];\n"
        # elif node.type == "string":
        #     return f"char {node.name}[];\n"
        # return f"{node.type} {node.name};\n"
        return f"{self.compute_type(node.type, node.name)};\n"

    def generate_C_code_ValueDefinition(self, node):
        # if node.pointer.type.startswith("["):
        #     if node.pointer.type[1:-1] == "string":
        #         return f"char {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        #     else:
        #         return f"{node.pointer.type[1:-1]} {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        # elif node.pointer.type == "string":
        #     return f"char {node.pointer.name}[] = {self.generate_C_code(node.pointer.value)};\n"
        # return f"{node.pointer.type} {node.pointer.name} = {self.generate_C_code(node.pointer.value)};\n"
        return f"{self.compute_type(node.pointer.type, node.pointer.name)} = {self.generate_C_code(node.pointer.value)};\n"

    def generate_C_code_ValueDeclaration(self, node):
        # if node.type.startswith("["):
        #     if node.type[1:-1] == "string":
        #         return f"char {node.name}[];\n"
        #     else:
        #         return f"{node.type[1:-1]} {node.name}[];\n"
        # elif node.type == "string":
        #     return f"char {node.name}[];\n"
        # return f"{node.type} {node.name};\n"
        return f"{self.compute_type(node.type, node.name)};\n"


    def generate_C_code_While(self, node):
        code = f"while ({self.generate_C_code(node.condition)}) {{\n"
        for statement in node.body:
            code += "\t" + self.generate_C_code(statement)
        code += "\t}\n"
        return code

    def generate_C_code_If(self, node):
        code = f"if ({self.generate_C_code(node.condition)}) {{\n"
        for statement in node.then_block:
            code += "\t" + self.generate_C_code(statement)
        code += "\t}\n"
        if node.else_block:
            code += "else {\n"
            for statement in node.else_block:
                code += "\t" + self.generate_C_code(statement)
            code += "\t}\n"
        return code

    def generate_C_code_IndexAccess(self, node):
        return f"{node.name}[{self.generate_C_code(node.index)}]"

    def generate_C_code_ReturnOrReassign(self, node):
        if isinstance(node.name, IndexAccess):
            return f"{node.name.name}[{self.generate_C_code(node.name.index)}] = {self.generate_C_code(node.value)};\n"
        else:
            if(node.name == self.context):
                if(node.name != "main"):
                    return f"return {self.generate_C_code(node.value)};\n"
                else:
                    return ""
            else:
                return f"{node.name} = {self.generate_C_code(node.value)};\n"

    def generate_C_code_FunctionCall(self, node):
        code = f"{node.name}("
        if node.arguments:
            for i, arg in enumerate(node.arguments):
                code += f"{self.generate_C_code(arg)}"
                if i < len(node.arguments) - 1:
                    code += ", "
        code += ");\n"
        return code

    def generate_C_code_Error(self, node):
        return f"// Error: {node.message}\n"
    
    def compute_type(self, var_type, name):
        if var_type.startswith("["):
            return self.compute_type(var_type[1:-1], name) + "[]"
        elif var_type == "string":
            return f"char {name}[]"
        else:
            return f"{var_type} {name}"
        
    def compute_return_type(self, ret_type):
        if ret_type.startswith("["):
            return self.compute_return_type(ret_type[1:-1]) + "*"
        elif ret_type == "string":
            return f"char*"
        else:
            return f"{ret_type}"

# codegen = CodeGenerator()
# c_code = codegen.generate(ast)
# print(c_code)

# with open('../generated/out.c', 'w') as file:
#     file.write(c_code)