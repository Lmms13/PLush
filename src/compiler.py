import sys
from lexer import test_lexer
from plush_parser import parse_data
from semantic_analysis import *

files = ['../test/0_valid/validTest.pl',
         '../test/0_valid/countOccurrences.pl',
         '../test/0_valid/isPalindrome.pl',
         '../test/0_valid/maxRangeSquared.pl',
         '../test/0_valid/sortArray.pl',
         '../test/1_lexical_error/countOccurrences1.pl',
         '../test/1_lexical_error/countOccurrences2.pl',
         '../test/1_lexical_error/isPalindrome1.pl',
         '../test/1_lexical_error/isPalindrome2.pl',
         '../test/1_lexical_error/maxRangeSquared1.pl',
         '../test/1_lexical_error/maxRangeSquared2.pl',
         '../test/1_lexical_error/sortArray1.pl',
         '../test/2_syntactic_error/countOccurrences1.pl',
         '../test/2_syntactic_error/countOccurrences2.pl',
         '../test/2_syntactic_error/isPalindrome1.pl',
         '../test/2_syntactic_error/maxRangeSquared1.pl',
         '../test/2_syntactic_error/sortArray1.pl',
         '../test/2_syntactic_error/sortArray2.pl',
         '../test/3_semantic_error/countOccurrences1.pl',
         '../test/3_semantic_error/isPalindrome1.pl',
         '../test/3_semantic_error/isPalindrome2.pl',
         '../test/3_semantic_error/maxRangeSquared1.pl',
         '../test/3_semantic_error/sortArray1.pl',
         '../test/3_semantic_error/sortArray2.pl']

if len(sys.argv) < 2:
    filepath = '../test/0_valid/countOccurrences.pl'
else:
    filepath = sys.argv[1]

with open(filepath, 'r') as file:
    data = file.read()

if not test_lexer(data):
    ast = parse_data(data)
    if ast is not None:
        SemanticAnalyzer(ast).analyze()
