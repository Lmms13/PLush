#include <stdio.h>
#include <math.h>

int array_length(int a[]);
void print_int(int str);
int countOccurrences(int n, int a[]) {
	int len = array_length(a);
	int i = 0;
	int count = 0;
	while (i < len) {
	if (a[i] == n) {
	count = count + 1;
	}
	i = i + 1;
	}
	return count;
}
int main(int argc, char *argv[]) {
	int a[] = {1, 2, 3, 4, 2, 6, 8, 2, 5, 7, 3, 2, 2, 1, 4, 5, 3, 2, 8, 10, 2};
	a[-1] = 1;
	int result = countOccurrences(2, a);
	print_int(result);
	return 0;
}
