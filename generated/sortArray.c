#include <stdio.h>
#include <math.h>

void print_int_array(int arr[], int size);
int* sortArray(int a[], int len) {
	int i = 1;
	int temp = 0;
	while (i < len) {
	if (a[i] < a[i - 1]) {
	temp = a[i];
	a[i] = a[i - 1];
	a[i - 1] = temp;
	i = 0;
	}
	i = i + 1;
	}
	return a;
}
int main(int argc, char *argv[]) {
	int len = 16;
	int a[16] = {6, 8, 4, 2, 4, 7, 1, 10, 8, 4, 9, 4, 3, 5, 2, 1};
	int* result = sortArray(a, len);
	print_int_array(result, len);
	return 0;
}
