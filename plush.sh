#!/bin/bash

# Get the filepath from the last command line argument
filepath=${!#}

# Get the file extension
extension="${filepath##*.}"

# Check if the file extension is not 'pl'
if [ "$extension" != "pl" ]; then
    echo "The PLush compiler only works for .pl files"
    exit 1
fi

# Extract the filename without the extension
filename=$(basename "$filepath" .pl)

# Initialize a flag variable
tree_flag=0

# Loop through all arguments
for arg in "$@"
do
    # Check if the current argument is --tree
    if [ "$arg" == "--tree" ]; then
        # Set the flag to 1 and break the loop
        tree_flag=1
        break
    fi
done

# If the flag is set to 1
if [ $tree_flag -eq 1 ]; then
    # Generate the AST and print it
    python3 ./src/compiler.py --tree "$filepath"

else
    #compiling and checking if the output is empty, meaning there are no errors
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