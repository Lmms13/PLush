function print_int_array(val arr: [int], val size: int);

function main(val args:[string]) {
    val rows : int := 3;
    val cols : int := 3;
    val matrix1 : [[int]] := [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    val matrix2 : [[int]] := [[10, 11, 12], [13, 14, 15], [16, 17, 18]];
    var result : [[int]] := [[0, 0, 0], [0, 0, 0], [0, 0, 0]];

    var i : int := 0;
    while i < rows {
        var j : int := 0;
        while j < cols {
            result[i][j] := matrix1[i][j] + matrix2[i][j];
            j := j + 1;
        }
        i := i + 1;
    }

    i := 0;
    while i < rows {
        print_int_array(result[i], cols);
        i := i + 1;
    }
}