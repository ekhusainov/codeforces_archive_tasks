from itertools import permutations
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


def sum_module_2(a, b):
    return (a + b) % 2


def arr_sum_model_2(arr1, arr2):
    total_arr = list(zip(arr1, arr2))
    return list(map(lambda x: sum_module_2(x[0], x[1]), total_arr))


def arr_010101(size):
    arr1 = []
    arr2 = []
    for i in range(size):
        arr1.append(i % 2)
        arr2.append((i + 1) % 2)
    return arr1, arr2


def main():
    t = int(input())
    for _ in range(t):
        alice_win, boris_win = map(int, input().split())
        match = alice_win * [1] + boris_win * [0]
        unique_mathces = list(set(permutations(match)))
        k_list = []
        total_mathces = alice_win + boris_win
        arr1, arr2 = arr_010101(total_mathces)
        for current_match in unique_mathces:
            k = sum(arr_sum_model_2(arr1, current_match))
            k_list.append(k)
            k = sum(arr_sum_model_2(arr2, current_match))
            k_list.append(k)
        k_list = list(set(k_list))
        k_list = sorted(k_list)
        print(len(k_list))
        print(*k_list)


if __name__ == "__main__":
    main()
