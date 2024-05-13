#declaration of function for FFI
function array_length(val a: [int]) : int;


#returning string instead of int
function countOccurrences(val n: int, val a: [int]) : string {
	val len : int := array_length(a);
	var i : int := 0;
	var count : int := 0; 
	while i < len {
        if a[i] = n {
			count := count + 1;
		}
		i := i + 1;
	} 
	countOccurrences := count;
}


function print_int(val str: int);


function main(val args:[string]) {
	val a : [int] := [1,2,3,4,2,6,8,2,5,7,3,2,2,1,4,5,3,2,8,10,2]; 
	val result : int := countOccurrences(2, a);
	print_int(result);
}