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


def main():
    t = int(input())
    for _ in " " * t:
        n = int(input())
        # segment_cost = []
        min_l = 1_000_000_001
        max_r = -1
        prev_answer = 1_000_000_001
        cost1 = 10_000_000_001
        cost2 = 10_000_000_001
        full_cost_from_one = 10_000_000_001
        for _ in " " * n:
            l, r, c = map(int, input().split())
            if l < min_l:
                min_l = l
            if r > max_r:
                max_r = r


            if min_l == l:
                if c < cost1:
                    cost1 = c
                if min_l == l and max_r == r:
                    if c < full_cost_from_one:
                        full_cost_from_one = c
            if max_r == r:
                if c < cost2:
                    cost2 = c
                if min_l == l and max_r == r:
                    if c < full_cost_from_one:
                        full_cost_from_one = c
            

            answer = min(cost1 + cost2, full_cost_from_one)
            # if answer == full_cost_from_one or answer == full_cost_from_one * 2:
            #     print(prev_answer)
            # else:
            print(answer)
            # print()
            prev_answer = answer
        # for i in answer:
        #     print(i)





if __name__ == "__main__":
    main()
