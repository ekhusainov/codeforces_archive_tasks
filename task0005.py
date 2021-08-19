"""
https://codeforces.com/problemset/problem/580/C
"""
from collections import defaultdict


def read_data():
    vertex_number, ignored_cats = map(int, input().split())
    vertex_with_cats = list(map(int, input().split()))
    tree = defaultdict(list)
    for _ in range(vertex_number - 1):
        node1, node2 = map(int, input().split())
        tree[node1 - 1].append(node2 - 1)
        tree[node2 - 1].append(node1 - 1)
    return vertex_number, ignored_cats, vertex_with_cats, tree


def dfs(tree, vertex, used, vertex_with_cats, ignored_cats, current_cats, list_cafe):
    used[vertex] = True
    if current_cats > ignored_cats:
        return list_cafe
    if vertex_with_cats[vertex] == 1:
        current_cats += 1
    else:
        current_cats = 0
    flag_leaf = 1
    for new_vertex in tree[vertex]:
        if not used[new_vertex]:
            flag_leaf = 0
            list_cafe = dfs(tree, new_vertex, used, vertex_with_cats,
                            ignored_cats, current_cats, list_cafe)
    if flag_leaf:
        list_cafe.append(vertex)
    return list_cafe


def main():
    vertex_number, ignored_cats, vertex_with_cats, tree = read_data()
    used = [False] * vertex_number
    list_cafe = []
    list_cafe = dfs(tree, 0, used, vertex_with_cats,
                    ignored_cats, 0, list_cafe)
    print(list_cafe)


if __name__ == "__main__":
    main()
