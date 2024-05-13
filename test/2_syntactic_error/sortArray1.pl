#declaration of function for FFI
function array_length(val a: [int]) : int;


function print_int_array(val arr: [int]);


function sortArray(var a: [int]) : [int]{
	val len : int := array_length(a);
	var i : int := 1;
	var temp : int := 0;

	while i < len {
		if a[i] < a[i-1] {
			temp := a[i];
			a[i] := a[i-1];
			#plus character
			a[i-1+] := temp;
			i := 0;
		}
		i := i + 1;
	}
	sortArray := a;
}


function main(val args:[string]) {
	var a : [int] := [6,8,4,2,4,7,1,10,8,4,9,4,3,5,2,1];
	val result : [int] := sortArray(a);
	print_int_array(result);
}