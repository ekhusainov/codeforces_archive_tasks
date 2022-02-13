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


def unioun_max_min(arr1, arr2):
    len1 = len(arr1)
    len2 = len(arr2)
    result = []
    if len1 > len2:
        for i in range(len2):
            result.append(arr1[i])
            result.append(arr2[i])
        result.append(arr1[len1 - 1])
    elif len1 == len2:
        for i in range(len2):
            result.append(arr1[i])
            result.append(arr2[i])
    else:
        for i in range(len1):
            result.append(arr2[i])
            result.append(arr1[i])
        result.append(arr2[len2 - 1])
    return result


from collections import defaultdict

def main():
    t = int(input())
    for _ in " " * t:
        n = int(input())
        p = list(map(int, input().split()))
        s = input()
        neg = []
        pos = []
        for idx, elem in enumerate(p):
            if s[idx] == "0":
                neg.append(elem)
            else:
                pos.append(elem)
        neg = sorted(neg)
        pos = sorted(pos)
        arr = neg + pos
        d = defaultdict(int)
        for i in range(n):
            d[arr[i]] = i + 1
        answer = []
        for i in range(n):
            answer.append(d[p[i]])
        print(*answer)


if __name__ == "__main__":
    main()
