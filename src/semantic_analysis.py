from plush_parser import *

print(ast)

var = Variable("a", Literal(1), "int")

print(var)
# class SemanticAnalyzer:
#     def __init__(self, ast):
#         self.ast = ast
#         self.errors = []

#     def analyze(self):
#         self.visit(self.ast)

#     def visit(self, node):
#         method_name = 'visit_' + type(node).__name__
#         visitor = getattr(self, method_name, self.generic_visit)
#         return visitor(node)

#     def generic_visit(self, node):
#         raise Exception('No visit_{} method'.format(type(node).__name__))

#     # Add methods for each node type here
#     # For example:
#     # def visit_VariableDeclaration(self, node):
#     #     pass

#     def get_errors(self):
#         return self.errors