#!/bin/bash

# Check if the first argument is --tree
if [ "$1" == "--tree" ]; then
    # Remove the first argument
    shift

    # Get the filename from the last command line argument
    filepath=${!#}

    # Extract the filename without the extension
    filename=$(basename "$filepath" .pl)

    # Generate the AST and print it
    python3 ./src/compiler.py --tree "$filepath"
else
    # Get the filename from the last command line argument
    filepath=${!#}

    # Extract the filename without the extension
    filename=$(basename "$filepath" .pl)

    output=$(python3 ./src/compiler.py "$filepath" | tee /dev/fd/2)

    if [ -z "$output" ]; then
        # Compile the C files to LLVM bitcode
        clang -emit-llvm -c ./generated/"$filename".c -o ./generated/"$filename".bc
        for file in ./lib/src/*.c
        do
            libname=$(basename "$file")
            clang -emit-llvm -c "$file" -o ./generated/lib/"${libname%.c}.bc"
        done

        # Link the LLVM bitcode files
        llvm-link ./generated/"$filename".bc ./generated/lib/*.bc -o ./generated/linked.bc

        # Optimize the linked LLVM bitcode
        opt -O3 ./generated/linked.bc -o ./generated/optimized.bc

        # Compile the linked LLVM bitcode to an executable
        clang ./generated/optimized.bc -o ./generated/"$filename" -lm

        # Run the executable
        ./generated/"$filename"

        # Cleanup
        #rm out.bc
        #rm linked.bc
        #rm optimized.bc
        for file in ./generated/*.bc
        do
            rm "$file"
        done
        for file in ./generated/lib/*.bc
        do
            rm "$file"
        done
    fi
fi