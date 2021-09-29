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


OUTPUT_FILEPATH = "somefile_0039.txt"
INPUT_FILEPATH = "weak_typing_chapter_2_input.txt"
MODULO = 1_000_000_007


def how_many_times_to_change_the_hand(our_string):
    answer_list = []
    answer = -1
    pred_chr = "init"
    for s in our_string:
        if s == "F":
            answer_list.append(max(answer, 0))
            continue
        if s != pred_chr:
            pred_chr = s
            answer += 1
        answer_list.append(max(answer, 0))
    answer = max(answer, 0)
    return answer_list


def main():
    with open(INPUT_FILEPATH, "r") as the_file:
        data_input = [line.rstrip() for line in the_file]
    finish_result = ""
    t = int(data_input[0])
    for idx in range(2, 2 * t + 1, 2):
        current_string = data_input[idx]
        answer = 0
        for i in range(len(current_string)):
            part_of_current_string = current_string[i:]
            answer = (answer + sum(how_many_times_to_change_the_hand(part_of_current_string))) % MODULO
        # part_answer = how_many_times_to_change_the_hand(current_string)
        # len_current = len(current_string)
        # for i in range(len_current):
        #     for j in range(i + 1, len_current + 1):
        #         sub_string = current_string[i: j]
        #         part_answer = (
        #             part_answer + how_many_times_to_change_the_hand(sub_string)) % MODULO
        finish_result = finish_result + "Case #" + \
            str(idx // 2) + ": " + str(answer) + "\n"
    if os.path.exists(OUTPUT_FILEPATH):
        os.remove(OUTPUT_FILEPATH)
    with open(OUTPUT_FILEPATH, "a") as the_file:
        the_file.write(finish_result)


if __name__ == "__main__":
    main()
