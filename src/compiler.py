import os
import sys
import json
from lexer import test_lexer
from plush_parser import parse_data
from semantic_analysis import *
from codegen import *

tree_flag = False 

if len(sys.argv) < 2:
    print("Usage:\nplush <filepath>\nplush --tree <filepath>")
else:
    if sys.argv[1] == '--tree':
        tree_flag = True       
    filepath = sys.argv[-1]

filename = os.path.splitext(os.path.basename(filepath))[0]

with open(filepath, 'r') as file:
    data = file.read()

if not test_lexer(data):
    parse_result = parse_data(data)
    ast = parse_result[0]
    parse_error = parse_result[1]
    if not parse_error and ast is not None:
        #there's some issue in the semantic analyzer that I couldn't 
        #find so it can't analyze the same ast, though it is the same data
        if SemanticAnalyzer(parse_data(data)[0]).analyze():
            c_code = CodeGenerator().generate(ast)
            if tree_flag:
                print(json.dumps(ast, default=lambda o: o.__dict__, indent=4))
            else:
                with open('./generated/'+filename+'.c', 'w') as file:
                    file.write(c_code)