#include <stdio.h>
#include <math.h>

void print_int_array(int arr[], int size);
int main(int argc, char *argv[]) {
	int rows = 3;
	int cols = 3;
	int matrix1[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
	int matrix2[3][3] = {{10, 11, 12}, {13, 14, 15}, {16, 17, 18}};
	int result[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
	int i = 0;
	while (i < rows) {
	int j = 0;
	while (j < cols) {
	result[i][j] = matrix1[i][j] + matrix2[i][j];
	j = j + 1;
	}
	i = i + 1;
	}
	i = 0;
	while (i < rows) {
	print_int_array(result[i], cols);
	i = i + 1;
	}
	return 0;
}
