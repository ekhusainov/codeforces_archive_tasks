"""
https://codeforces.com/problemset/problem/1/A
"""
from math import ceil


def main():
    n, m, a = map(int, input().spt())
    width = ceil(n / a)
    height = ceil(m / a)
    print(width * height)


if __name__ == "__main__":
    main()
