function print_int_array(val arr: [int], val size: int);

function sortArray(var a: [int], val len:int) : [int]{
	var i : string := 1;
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


function main(val args:[string]) {
	val len : int := 16;
	var a : [int] := [6,8,4,2,4,7,1,10,8,4,9,4,3,5,2,1];
	val result : [int] := sortArray(a, len);
	print_int_array(result, len);
}