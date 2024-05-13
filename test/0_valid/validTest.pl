function countOccurrences(val n: int, val a: [int]) : int {
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

function main(val args:[string]) {
	val result : int := countOccurrences(1, [1,2,3]);
	print_int(result);
}
