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


FAIL = -1


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(lambda x: int(x) % 2, input().split()))
        sum_arr = sum(arr)

        half_n = n // 2
        if n % 2:
            if half_n != sum_arr and sum_arr != (half_n + 1):
                print(FAIL)
                continue
        else:
            if half_n != sum_arr:
                print(FAIL)
                continue

        if n % 2:
            if sum_arr == half_n:  # 0 1 0
                etalon_arr = list(range(0, n, 2))
                where_now_0 = [i for i, x in enumerate(arr) if x == 0]
                ans = 0
                for i in range(len(etalon_arr)):
                    ans += abs(etalon_arr[i] - where_now_0[i])
                print(ans)
                continue
            else:
                etalon_arr = list(range(0, n, 2))  # 1 0 1
                where_now_0 = [i for i, x in enumerate(arr) if x == 1]
                ans = 0
                for i in range(len(etalon_arr)):
                    ans += abs(etalon_arr[i] - where_now_0[i])
                print(ans)
                continue
        else:
            etalon_arr = list(range(0, n, 2))
            where_now_0 = [i for i, x in enumerate(arr) if x == 0]
            ans1 = 0
            for i in range(len(etalon_arr)):
                ans1 += abs(etalon_arr[i] - where_now_0[i])
            etalon_arr = list(range(1, n, 2))
            where_now_1 = [i for i, x in enumerate(arr) if x == 0]
            ans2 = 0
            for i in range(len(etalon_arr)):
                ans2 += abs(etalon_arr[i] - where_now_1[i])
            print(min(ans1, ans2))


if __name__ == "__main__":
    main()
