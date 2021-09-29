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


def main():
    t = int(input())
    for _ in range(t):
        __ = input()
        first_string = input()
        second_string = input()
        answer = 0
        need_look_prev = 0
        for i in range(len(first_string)):
            current = int(first_string[i]) + int(second_string[i])

            if i == 0:
                if current == 1:
                    answer += 2
                elif current == 2:
                    prev_elem = current
                    need_look_prev = 1
                else:
                    prev_elem = current
                    need_look_prev = 1
                continue
            if need_look_prev:
                if current == 1:
                    if prev_elem == 2:
                        answer += 2
                        need_look_prev = 0
                        continue
                    else:
                        answer += 3
                        need_look_prev = 0
                        continue
                elif current == 2:
                    if prev_elem == 0:
                        answer += 2
                        need_look_prev = 0
                        continue
                    elif prev_elem == 2:
                        continue
                else:
                    if prev_elem == 2:
                        answer += 2
                        need_look_prev = 0
                        continue
                    else:
                        answer += 1
                        continue
            if need_look_prev == 0:
                if current == 1:
                    answer += 2
                elif current == 2:
                    prev_elem = current
                    need_look_prev = 1
                else:
                    prev_elem = current
                    need_look_prev = 1
                continue
        if current == 0:
            answer += 1

        answer_2 = 0
        need_look_prev = 0
        for i in range(len(first_string) - 1, -1, -1):
            current = int(first_string[i]) + int(second_string[i])

            if i == 0:
                if current == 1:
                    answer_2 += 2
                elif current == 2:
                    prev_elem = current
                    need_look_prev = 1
                else:
                    prev_elem = current
                    need_look_prev = 1
                continue
            if need_look_prev:
                if current == 1:
                    if prev_elem == 2:
                        answer_2 += 2
                        need_look_prev = 0
                        continue
                    else:
                        answer_2 += 3
                        need_look_prev = 0
                        continue
                elif current == 2:
                    if prev_elem == 0:
                        answer_2 += 2
                        need_look_prev = 0
                        continue
                    elif prev_elem == 2:
                        continue
                else:
                    if prev_elem == 2:
                        answer_2 += 2
                        need_look_prev = 0
                        continue
                    else:
                        answer_2 += 1
                        continue
            if need_look_prev == 0:
                if current == 1:
                    answer_2 += 2
                elif current == 2:
                    prev_elem = current
                    need_look_prev = 1
                else:
                    prev_elem = current
                    need_look_prev = 1
                continue
        if current == 0:
            answer_2 += 1
        print(max(answer, answer_2))


if __name__ == "__main__":
    main()
