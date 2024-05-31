#include <stdio.h>
#include <math.h>

void print_int(int str);
int array_length(int a[]);
int getLeftChildIndex(int i) {
	return 2 * i + 1;
}
int getRightChildIndex(int i) {
	return 2 * i + 2;
}
void dfs(int node, int tree[]) {
	if (node >= array_length(tree)) {
	return ;
	}
	print_int(tree[node]);
	dfs(getLeftChildIndex(node), tree);
	dfs(getRightChildIndex(node), tree);
}
int main(int argc, char *argv[]) {
	int tree[7] = {1, 2, 3, 4, 5, 6, 7};
	dfs(0, tree);
	return 0;
}
