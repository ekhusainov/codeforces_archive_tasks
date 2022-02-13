from collections import defaultdict
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


def bin_range(bin1, bin2):
    answer = 0
    for i in range(len(bin1)):
        if bin1[i] != bin2[i]:
            answer += 1
    return answer


def bin_values(l, arr):
    answer = []
    for i in arr:
        current_bin = bin(i)[2:]
        current_bin = (l - len(current_bin)) * "0" + current_bin
        answer.append(current_bin)
    return answer


def main():
    t = int(input())
    for _ in " " * t:
        n, l = map(int, input().split())
        arr = list(map(int, input().split()))
        bin_arr = bin_values(l, arr)
        bin_answer = ""
        for i in range(l):
            d = defaultdict(int)
            
            for j in bin_arr:
                d[j[i]] += 1
            
            bin_answer = bin_answer + sorted(list(d.items()), key=lambda x: x[1])[-1][0]
        print(int(bin_answer, 2))

if __name__ == "__main__":
    main()
