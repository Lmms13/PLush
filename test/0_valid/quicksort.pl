function print_int_array(val arr: [int], val size: int);

function swap(var a: [int], val i: int, val j: int) : [int] {
    val temp : int := a[i];
    a[i] := a[j];
    a[j] := temp;
    swap := a;
}

function partition(var a: [int], val low: int, val high: int) : int {
    val pivot : int := a[high];
    var i : int := low - 1;
    var j : int := low;
    while j <= high - 1 {
        if a[j] < pivot {
            i := i + 1;
            a := swap(a, i, j);
        }
        j := j + 1;
    }
    a := swap(a, i + 1, high);
    partition := i + 1;
}

function quicksort(var a: [int], val low: int, val high: int) : [int] {
    if low < high {
        val pi : int := partition(a, low, high);
        a := quicksort(a, low, pi - 1);
        a := quicksort(a, pi + 1, high);
    }
    quicksort := a;
}

function main(val args:[string]) {
    val len : int := 13;
    val a : [int] := [10, 7, 8, 9, 1, 13, 5, 3, 12, 6, 11, 2, 4];
    quicksort(a, 0, len - 1);
    print_int_array(a, len);
}