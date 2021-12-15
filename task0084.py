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


def main():
    t = int(input())
    for _ in " " * t:
        n = int(input())
        arr = list(map(int, input().split()))
        fl = 1
        # prew = 0
        for i, elem in enumerate(arr):
            if i == 0:
                prew = elem
                if elem == 1:
                    fl += 1
                continue
            if elem == 0 and prew == 0:
                fl = -1
                break
            if elem == 1 and prew == 0:
                fl += 1
                prew = elem
                continue
            if elem == 0 and prew == 1:
                prew = elem
                continue
            if elem == 1 and prew == 1:
                fl += 5
                prew = elem
                continue

        print(fl)


if __name__ == "__main__":
    main()
