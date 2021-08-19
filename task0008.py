import sys
from math import sqrt, ceil


def read_data():
    data = sys.stdin.read().split("\n")
    return data[1:-1]


def get_coords(value):
    circle = ceil(sqrt(value))
    middle = (circle - 1) * circle + 1
    if value == middle:
        return circle, circle
    if value < middle:
        return circle - middle + value, circle
    return circle, circle - (value - middle)


def main():
    data = read_data()
    answer = ""
    for i in data:
        x, y = get_coords(int(i))
        answer += str(x) + " " + str(y) + "\n"



    sys.stdout.write(answer[:-1])


if __name__ == "__main__":
    main()
