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
    primes = []
    for num in range(2, 10_001):
        if all(num % i != 0 for i in range(2, num)):
            primes.append(num)
    t = int(input())
    for _ in " " * t:
        answer = 0
        n, e = map(int, input().split())
        arr = list(map(int, input().split()))
        mul_values = 1
        have_prime = 0
        for i in range(n - 1):
            value = arr[i]
            have_prime = 0
            if value == 1:
                current_idx = i
                while current_idx < n:
                    current_idx += e
                    if have_prime:
                        try:
                            if arr[current_idx] == 1:
                                answer += 1
                                # current_idx = current_idx + e
                                continue
                            else:
                                break
                        except IndexError:
                            break
                    try:
                        if arr[current_idx] in primes:
                            have_prime = 1
                            answer += 1
                        elif arr[current_idx] == 1:
                            continue
                    except IndexError:
                        break
            elif value in primes:
                current_idx = i
                while current_idx < n:
                    current_idx += e
                    try:
                        if arr[current_idx] == 1:
                            answer += 1
                            # current_idx = current_idx + e
                            continue
                        else:
                            break
                    except IndexError:
                        break
            else:
                continue
        print(answer)


if __name__ == "__main__":
    main()
