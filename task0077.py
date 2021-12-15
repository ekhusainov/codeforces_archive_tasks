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


def count_2_div(n):
    times = 0
    while n % 2 == 0:
        n = n // 2
        times += 1
    return times


def get_area(our_string, idx):
    n = len(our_string)
    values = list(range(idx - 2, idx + 3))
    if values[4] >= n:
        del values[4]
    if values[3] >= n:
        del values[3]
    if values[1] < 0:
        del values[1]
    if values[0] < 0:
        del values[0]
    sub_string = []
    for i in values:
        sub_string.append(our_string[i])

    return "".join(sub_string)


def main():
    n, q = map(int, input().split())
    our_string = input()
    init_count = our_string.count("abc")
    list_string = list(our_string)
    for _ in " " * q:
        i, s = input().split()
        i = int(i) - 1
        # current_string = "".join(list_string)
        area_1 = get_area(list_string, i)
        list_string[i] = s
        # current_string = "".join(list_string)
        area_2 = get_area(list_string, i)
        count_1 = area_1.count("abc")
        count_2 = area_2.count("abc")
        init_count = init_count - count_1 + count_2
        print(init_count)

        # answer = current_string.count("abc")
        # print(answer)


if __name__ == "__main__":
    main()
