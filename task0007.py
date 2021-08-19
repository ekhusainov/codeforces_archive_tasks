import sys


def get_d(a, b, c):
    diff = abs(a - b)
    if (a + b) % 2 == 1:
        return -1
    if c <= diff:
        return diff + c
    if diff * 2 < c:
        return -1
    if c - diff == a or c - dicc == b:
        return -1
    return c - diff

def read_data():
    data = sys.stdin.read().split("\n")
    return data[1:-1]


def main():
    data = read_data()
    answer = ""
    for i in data:
        a, b, c = map(int, i.split())
        d = str(get_d(a, b, c)) + "\n"
        answer += d 

    answer = answer[:-1]
    sys.stdout.write(answer)

if __name__ == "__main__":
    main()