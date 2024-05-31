function print_int(val str: int);

function getLeftChildIndex(val i: int) : int {
    getLeftChildIndex := 2*i + 1;
}

function getRightChildIndex(val i: int) : int {
    getRightChildIndex := 2*i + 2;
}

function dfs(val node: int, val tree: [int], val len: int) {
    if node >= len {
        dfs := void;
    }
    print_int(tree[node]);
    dfs(getLeftChildIndex(node), tree, len);
    dfs(getRightChildIndex(node), tree, len);
}

function main(val args:[string]) {
    val len: int := 7; 
    val tree : [int] := [1, 2, 3, 4, 5, 6, 7];
    dfs(0, tree, len);
}