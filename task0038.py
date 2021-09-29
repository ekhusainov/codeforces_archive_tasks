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


OUTPUT_FILEPATH = "somefile_0038.txt"
INPUT_FILEPATH = "weak_typing_chapter_1_input.txt"


def how_many_times_to_change_the_hand(our_string):
    answer = -1
    pred_chr = "init"
    for s in our_string:
        if s == "F":
            continue
        if s != pred_chr:
            pred_chr = s
            answer += 1
    answer = max(answer, 0)
    return answer


def main():
    # t = int(input())
    with open(INPUT_FILEPATH, "r") as the_file:
        data_input = [line.rstrip() for line in the_file]
    answer = ""
    t = int(data_input[0])
    for i in range(2, 2 * t + 1, 2):
        part_answer = how_many_times_to_change_the_hand(data_input[i])
        answer = answer + "Case #" + \
            str(i // 2) + ": " + str(part_answer) + "\n"
    if os.path.exists(OUTPUT_FILEPATH):
        os.remove(OUTPUT_FILEPATH)
    with open(OUTPUT_FILEPATH, "a") as the_file:
        the_file.write(answer)
    # for i in range(t):
    #     n = int(input())
    #     current_string = input()
    #     part_answer = -1
    #     pred_chr = "init"
    #     for s in current_string:
    #         if s == "F":
    #             continue
    #         if s != pred_chr:
    #             pred_chr = s
    #             part_answer += 1
    #     part_answer = max(part_answer, 0)
    #     answer = answer + "Case #" + \
    #         str(i + 1) + ": " + str(part_answer) + "\n"

    # if os.path.exists(OUTPUT_FILEPATH):
    #     os.remove(OUTPUT_FILEPATH)
    # with open(OUTPUT_FILEPATH, "a") as the_file:
    #     the_file.write(answer)


if __name__ == "__main__":
    main()
