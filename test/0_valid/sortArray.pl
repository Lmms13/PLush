function sortArray(val a: [int]) : [int]{
	val len : int := array_length(a);
	var i : int := 1;
	var temp : int := 0;

	while i < len {
		if a[i] < a[i-1] {
			temp := a[i];
			a[i] := a[i-1];
			a[i-1] := temp;
			i := 0;
		}
		i := i + 1;
	}
	sortArray := a;
}

#declaration of function for FFI
function array_length(val a: [int]) : int;


function main(val args:[string]) {
	#I don't know how to initialize an array in this language since there is no example available.
	#I assume that it's either something like this or maybe we also need to specify the length of 
	#the array given we should also be able to initialize an empty array

	val a : [int] := [6,8,4,2,4,7,1,10,8,4,9,4,3,5,2,1];
	val result : int := sortArray(a);
	print_int(result);
}