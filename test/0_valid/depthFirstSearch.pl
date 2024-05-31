function print_int(val str: int);

function array_length(val a: [int]) : int;

function getLeftChildIndex(val i: int) : int {
    getLeftChildIndex := 2*i + 1;
}

function getRightChildIndex(val i: int) : int {
    getRightChildIndex := 2*i + 2;
}

function dfs(val node: int, val tree: [int]) {
    if node >= array_length(tree) {
        dfs := void;
    }
    print_int(tree[node]);
    dfs(getLeftChildIndex(node), tree);
    dfs(getRightChildIndex(node), tree);
}

function main(val args:[string]) {
    val tree : [int] := [1, 2, 3, 4, 5, 6, 7];
    dfs(0, tree);
}