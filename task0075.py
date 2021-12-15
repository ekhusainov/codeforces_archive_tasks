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

from collections import deque

def main():
    t = int(input())
    for _ in " " * t:
        n = int(input())
        arr = list(map(int, input().split()))
        arr_ext = []
        for idx, elem in enumerate(arr):
            arr_ext.append((elem, idx + 1))
        arr_ext = sorted(arr_ext, key=lambda x: x[0], reverse=True)
        ans = deque()
        ans.append((0, 0))
        i = 0
        result = 0
        range_b = 1
        while i < n:
            
            ans.appendleft(arr_ext[i])
            result += 2 * arr_ext[i][0] * range_b
            i += 1
            if i == n:
                break
            ans.append(arr_ext[i])
            result += 2 * arr_ext[i][0] * range_b
            i += 1
            range_b += 1
        tru_ans = []
        for idx, elem in enumerate(ans):
            tru_ans.append((elem[0], elem[1], idx))
        tru_ans = sorted(tru_ans, key=lambda x: x[1])
        fin_ans = []
        for i in tru_ans:
            fin_ans.append(i[2])
        print(result)
        print(*fin_ans)
        



if __name__ == "__main__":
    main()
