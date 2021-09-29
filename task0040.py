from sys import stdout, stdin
from io import IOBase, BytesIO
from os import read, write, fstat
import os

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


OUTPUT_FILEPATH = "somefile_0040.txt"
INPUT_FILEPATH = "traffic_control_input.txt"
MAX_VALUE = 1000


def get_an_array_of_borders(sum_value, count_value):
    min_value = sum_value // count_value
    answer = [min_value] * (count_value - 1)
    last_elem = sum_value - min_value * (count_value - 1)
    answer.append(last_elem)
    return answer


def main():
    with open(INPUT_FILEPATH, "r") as the_file:
        data_input = [line.rstrip() for line in the_file]
    finish_result = ""
    t = int(data_input[0])
    for idx in range(1, t + 1):
        n, m, a, b = map(int, data_input[idx].split())

        if n + m - 1 > a or n + m - 1 > b:
            finish_result = finish_result + "Case #" + \
                str(idx) + ": Impossible\n"
            continue
        finish_result = finish_result + "Case #" + \
            str(idx) + ": Possible\n"
        first_raw = [1] * m
        first_raw = list(map(str, first_raw))
        first_raw = " ".join(first_raw)
        finish_result = finish_result + first_raw + "\n"
        left_border = get_an_array_of_borders(b - m, n - 1)
        right_border = get_an_array_of_borders(a - m, n - 1)

        for i in range(n - 1):
            current_raw = [MAX_VALUE] * (m - 2)
            current_raw.append(right_border[i])
            current_raw.insert(0, left_border[i])
            current_raw = list(map(str, current_raw))
            current_raw = " ".join(current_raw)
            finish_result = finish_result + current_raw + "\n"

    if os.path.exists(OUTPUT_FILEPATH):
        os.remove(OUTPUT_FILEPATH)
    with open(OUTPUT_FILEPATH, "a") as the_file:
        the_file.write(finish_result)


if __name__ == "__main__":
    main()
