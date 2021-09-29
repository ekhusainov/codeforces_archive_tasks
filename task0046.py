"""
https://codeforces.com/problemset/problem/20/C?locale=ru
"""
from heapq import heappop, heappush
from sys import stdout, stdin
from io import IOBase, BytesIO
from os import read, write, fstat

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self, size: int = ...):
        while self.newlines == 0:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def print(*args, **kwargs):
    """Prints the values to a stream, or to sys.stdout by default."""
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()


stdin, stdout = IOWrapper(stdin), IOWrapper(stdout)
def input(): return stdin.readline().rstrip("\r\n")


INF = float("inf")


def read_data():
    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        node1, node2, weight = map(int, input().split())
        node1 -= 1
        node2 -= 1
        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))
    return n, graph


def dijkstra(graph, start=0):
    n = len(graph)
    dist, parents_list = [INF] * n, [-1] * n
    dist[start] = 0

    queue = [(0, start)]
    while queue:
        path_len, v = heappop(queue)
        if path_len == dist[v]:
            for (w, edge_len) in graph[v]:
                if edge_len + path_len < dist[w]:
                    dist[w], parents_list[w] = edge_len + path_len, v
                    heappush(queue, (edge_len + path_len, w))
    return parents_list


def main():
    n, graph = read_data()
    parents_list = dijkstra(graph)
    if parents_list[n - 1] == -1:
        print(-1)
    else:
        full_path, parent = [], n - 1
        while parent != parents_list[0]:
            full_path.append(parent + 1)
            parent = parents_list[parent]
        full_path.reverse()
        print(*full_path)


if __name__ == "__main__":
    main()
