function array_length(val a: [int]) : int;

function print_int(val str: int);

function cast_float_to_int(var n : float) : int; 

function binary_search(val a: [int], val low: int, val high: int, val target: int) : int {
    if high >= low {
        val mid : int := cast_float_to_int(low + (high - low) / 2);
        if a[mid] = target {
            binary_search := mid;
        } 
        else {
            if a[mid] > target {
                binary_search := binary_search(a, low, mid - 1, target);
            } 
            else {
                binary_search := binary_search(a, mid + 1, high, target);
            }
        }
    } 
    else {
        binary_search := -1;
    }
}

function main(val args:[string]) {
    val a : [int] := [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    val target : int := 7;
    val result : int := binary_search(a, 0, array_length(a) - 1, target);
    print_int(result);
}