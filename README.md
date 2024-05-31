Luís Santos 56341

Note about the submission:
- I just zipped the folder with the .git file and delivered it. I'm not sure if that was the correct way to submit the project, but I didn't see what else "You will submit a zip folder that contains a git repo" could mean.

# PLush

setup.sh: 
- script to install the necessary dependencies to run the compiler, it launches a docker container
- execute with `./setup.sh`

plush.sh: 
- script to run the compiler. The line to execute the resulting program (line 60) is commented, uncomment it to run the program 
- inside the container, it can be executed with the commands:
    - `plush <file.pl>` to compile a file and generate the C file and the binary file
    - `plush -tree <file.pl>` to compile and print a JSON representation of the AST
    - notes: 
        - the last argument must be the filepath to the PLush file (as stated in the project definition)
        - the --tree flag can be anywhere (as stated in the project definition), but not in the last position, because that's where the .pl file should be (as stated in the project definition)
        - all the other arguments are ignored

Dockerfile:
- file to build the docker container, used in `setup.sh`

src:
- contains the files:
    - lexer.py: lexer for the PLush language
    - parser.py: syntatic parser for the PLush language
    - semantic_analysis.py: typechecking and semantic analysis for the PLush language
    - codegen.py: code generation from PLush to C
    - compiler.py: main file to run the compiler, calling every step in order

lib:
- contains the custom C libraries linked with the compiled code
- src contains the source code for the libraries
- include contains the header files for the libraries

generated:
- contains the generated C code from the PLush code
- contains the binary files generated using LLVM, which can be executed
- the lib directory is used in the compiling stage, but the files stored there are deleted after the compilation

test:
- 0_valid: contains valid PLush programs to test the compiler, plus the expected output for each program
- 1_lexical_error: contains PLush programs with lexical errors to test the lexer
- 2_syntactic_error: contains PLush programs with syntactic errors to test the parser
- 3_semantic_error: contains PLush programs with semantic errors to test the typechecker
