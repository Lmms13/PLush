function isPalindrome(val str:? string) : int {
    val len: int := string_length(str);
    var i : int := 0;
	while i <= (len / 2) {
        if string_get_char_at(str, i) != string_get_char_at(str, (len - i - 1))  {
			isPalindrome := 0;
		}
	} 
	isPalindrome := 1;
}

#bool is not one of the types enumerated in the project description, but it does mention
#boolean literals, so I am unsure if it is in fact a type or if we use booleans like in C,
#with 0 and 1. So I wrote both versions and I suppose the professor can consider whichever
#one is actually in line with the project definition.

# function isPalindrome(val str:? string) : bool {
#   val len: int := string_length(str);
#   var i : int := 0;
# 	while i <= (len / 2) {
#         if string_get_char_at(str, i) != string_get_char_at(str, (len - i - 1))  {
# 			isPalindrome := false;
# 		}
# 	} 
# 	isPalindrome := true;
# }

#declaration of function for FFI
function string_length(val str: string) : int;

#declaration of function for FFI
function string_get_char_at(val str: string, val index: int) : str;


function main(val args:[string]) {
	val str : string := "racecar"; 
	val result : int := isPalindrome(str);
	#val result : bool := isPalindrome(str);
	print_int(result);
}
