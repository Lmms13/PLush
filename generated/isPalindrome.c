#include <stdio.h>
#include <math.h>

int string_length(char str[]);
char string_get_char_at(char str[], int index);
void print_boolean(int str);
int isPalindrome(char str[]) {
	int len = string_length(str);
	int i = 0;
	while (i <= len / 2) {
	if (string_get_char_at(str, i) != string_get_char_at(str, len - i - 1)) {
	return 0;
	}
	i = i + 1;
	}
	return 1;
}
int main(int argc, char *argv[]) {
	char str[] = "racecar";
	int result = isPalindrome(str);
	print_boolean(result);
	return 0;
}
