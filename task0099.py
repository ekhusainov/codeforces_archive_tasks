from ast import Index
from sys import stdout, stdin
from io import IOBase, BytesIO
from os import read, supports_follow_symlinks, write, fstat

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

from collections import defaultdict

def main():
    t = int(input())
    for _ in " " * t:
        n = int(input())
        tree = defaultdict(list)
        need_break = 0
        edges = list(range(1, n + 1))
        init_edges = []
        for _ in " " * (n - 1):
            a, b = map(int, input().split())
            tree[a].append(b)
            tree[b].append(a)
            init_edges.append((a, b))
            if len(tree[a]) == 3 or len(tree[b]) == 3:
                need_break = 1
                continue
            if len(tree[a]) == 2:
                edges.remove(a)
            if len(tree[b]) == 2:
                edges.remove(b)
        if need_break:
            print(-1)
            break
        start_edge = edges[0]
        path = defaultdict(int)
        current_node = start_edge
        edges = list(range(1, n + 1))
        edges.remove(start_edge)
        current_weight = 3
        while True:
            try:
                try:
                    sec_node = tree[current_node][0]
                    edges.remove(sec_node)
                except ValueError:
                    sec_node = tree[current_node][1]
                    edges.remove(sec_node)
                prev_node = current_node
            except IndexError:
                break
            if current_weight == 2:
                current_weight = 3
            else:
                current_weight = 2
            path[(current_node, sec_node)] = current_weight
            path[(sec_node, current_node)] = current_weight
            current_node = sec_node
        answer = []
        for i in init_edges:
            answer.append(path[i])
        print(*answer)



if __name__ == "__main__":
    main()
