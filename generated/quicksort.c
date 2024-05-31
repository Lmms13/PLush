#include <stdio.h>
#include <math.h>

void print_int_array(int arr[], int size);
int* swap(int a[], int i, int j) {
	int temp = a[i];
	a[i] = a[j];
	a[j] = temp;
	return a;
}
int partition(int a[], int low, int high) {
	int pivot = a[high];
	int i = low - 1;
	int j = low;
	while (j <= high - 1) {
	if (a[j] < pivot) {
	i = i + 1;
	a = swap(a, i, j);
	}
	j = j + 1;
	}
	a = swap(a, i + 1, high);
	return i + 1;
}
int* quicksort(int a[], int low, int high) {
	if (low < high) {
	int pi = partition(a, low, high);
	a = quicksort(a, low, pi - 1);
	a = quicksort(a, pi + 1, high);
	}
	return a;
}
int main(int argc, char *argv[]) {
	int len = 13;
	int a[13] = {10, 7, 8, 9, 1, 13, 5, 3, 12, 6, 11, 2, 4};
	quicksort(a, 0, len - 1);
	print_int_array(a, len);
	return 0;
}
