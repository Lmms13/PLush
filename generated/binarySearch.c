#include <stdio.h>
#include <math.h>

int array_length(int a[]);
void print_int(int str);
int cast_float_to_int(float n);
int binary_search(int a[], int low, int high, int target) {
	if (high >= low) {
	int mid = cast_float_to_int(low + high - low / 2);
	if (a[mid] == target) {
	return mid;
	}
else {
	if (a[mid] > target) {
	return binary_search(a, low, mid - 1, target);
	}
else {
	return binary_search(a, mid + 1, high, target);
	}
	}
	}
else {
	return -1;
	}
}
int main(int argc, char *argv[]) {
	int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	int target = 7;
	int result = binary_search(a, 0, array_length(a) - 1, target);
	print_int(result);
	return 0;
}
