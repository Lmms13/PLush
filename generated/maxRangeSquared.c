#include <stdio.h>
#include <math.h>

int actual_min = -9;
int actual_max = 9;
int maxRangeSquared(int mi, int ma) {
	int current_max = pow(mi, 2);
	while (mi <= ma) {
	int current_candidate = pow(mi, 2);
	if (current_candidate > current_max) {
	current_max = current_candidate;
	}
	}
	return current_max;
}
void print_int(int str);
int main(int argc, char *argv[]) {
	int result = maxRangeSquared(actual_min, actual_max);
;
	print_int(result);
	return 0;
}
