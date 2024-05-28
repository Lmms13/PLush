import os
import sys
from lexer import test_lexer
from plush_parser import parse_data
from semantic_analysis import *
from codegen import *

if len(sys.argv) < 2:
    filepath = '../test/0_valid/countOccurrences.pl'
else:
    filepath = sys.argv[1]

filename = os.path.splitext(os.path.basename(filepath))[0]

with open(filepath, 'r') as file:
    data = file.read()

if not test_lexer(data):
    ast = parse_data(data)
    if ast is not None:
        #there's some issue in the semantic analyzer that I couldn't 
        #find so it can't analyze the same ast
        if SemanticAnalyzer(parse_data(data)).analyze():
            c_code = CodeGenerator().generate(ast)
            # print(c_code)

            with open('./generated/'+filename+'.c', 'w') as file:
                file.write(c_code)
