#include <string.h>
#include <stdio.h>

int string_length(char* str) {
    return strlen(str);
}

char string_get_char_at(char* str, int index) {
    return str[index];
}

void print_boolean(int b) {
    if (b) {
        printf("true\n");
    } else {
        printf("false\n");
    }
}