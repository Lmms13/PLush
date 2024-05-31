#include <stdio.h>

void print_int(int str){
  printf("%d\n", str);
}

int cast_float_to_int(float n){
  return (int) n;
}

void print_boolean(int b) {
    if (b) {
        printf("true\n");
    } else {
        printf("false\n");
    }
}