#declaration of function for FFI
function string_length(val str: string) : int;


#declaration of function for FFI
function string_get_char_at(val str: string, val index: int) : char;


function print_boolean(val str: boolean);


function isPalindrome(val str: string) : boolean {
  val len: int := string_length(str);
  var i : int := 0;
	while i <= (len / 2) {
        if string_get_char_at(str, i) != string_get_char_at(str, (len - i - 1))  {
			isPalindrome := false;
		}
	} 
	isPalindrome := true;
}


function main(val args:[string]) {
	#float instead of string
	val str : float := "racecar"; 
	val result : boolean := isPalindrome(str);
	print_boolean(result);
}