function array_length(val a: [int]) : int;

function print_int(val str: int);

function dfs(val node: int, val visited: [int], val graph: [[int]]) {
    visited[node] := 1;
    print_int(node);
    val i : int := 0;
    while i < array_length(graph[node]) {
        if visited[graph[node][i]] == 0 {
            dfs(graph[node][i], visited, graph);
        }
        i := i + 1;
    }
}

function main(val args:[string]) {
    val graph : [[int]] := [[1, 2], [0, 3, 4], [0, 4], [1, 4, 5], [1, 2, 3, 5], [3, 4]];
    val visited : [int] := [0, 0, 0, 0, 0, 0];
    dfs(0, visited, graph);
}

#0 1 3 4 2 5