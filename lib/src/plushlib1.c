#include <stdio.h>

int array_length(int a[]) { 
  int i; 
  int count = 0; 
  for(i=0; a[i]!='\0'; i++) { 
    count++; 
  } 
  return count; 
}